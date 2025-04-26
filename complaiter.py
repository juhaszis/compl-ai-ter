import sys
import os
import requests
import json
import ast
import re

# 🔧 Configuration via environment variables
OLLAMA_API = "http://localhost:11434/api/generate"
MANAI_API = os.getenv("COMPL_AI_TER_MANAI_API", "http://localhost:8000/query")
DEFAULT_MODEL = os.getenv("COMPL_AI_TER_MODEL", "codellama:13b")
DEFAULT_MAX_SUGGESTIONS = int(os.getenv("COMPL_AI_TER_MAX", 3))
DEFAULT_OS = os.getenv("COMPL_AI_TER_OS", "Ubuntu Linux")
DEFAULT_DEBUG = os.getenv("COMPL_AI_TER_DEBUG", "0") == "1"
USE_MANAI = os.getenv("COMPL_AI_TER_USE_MANAI", "1") == "1"
PROMPT_FILE = os.getenv("COMPL_AI_TER_PROMPT", os.path.expanduser("~/.se/system_prompt.txt"))
USER_PROMPT_PREFIX_FILE = os.getenv("COMPL_AI_TER_USER_PROMPT_PREFIX", os.path.expanduser("~/.se/user_prompt_prefix.txt"))
RAW_PROMPT_FILE = os.getenv("COMPL_AI_TER_SYSTEM_PROMPT_RAW", os.path.expanduser("~/.se/system_prompt_raw.txt"))

# 🖥️ Detect the operating system from /etc/os-release
def detect_os():
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    return line.strip().split("=", 1)[1].strip('"')
    except:
        pass
    return DEFAULT_OS

# 📄 Load system prompt text from a file
def load_system_prompt():
    try:
        with open(PROMPT_FILE, "r") as f:
            return f.read().strip()
    except:
        return "You are a helpful tool that completes or corrects shell commands."

# 📄 Load raw system prompt text from a file
def load_raw_prompt():
    try:
        with open(RAW_PROMPT_FILE, "r") as f:
            return f.read().strip()
    except:
        return "You are a raw execution helper."

# 📄 Load user prompt prefix from a file
def load_user_prompt_prefix():
    try:
        with open(USER_PROMPT_PREFIX_FILE, "r") as f:
            return f.read().strip()
    except:
        return "Correct and complete this shell command:"

# 🔹 Fetch additional context from local manai service
def get_manai_context(question):
    try:
        response = requests.post(
            MANAI_API,
            headers={"Content-Type": "application/json"},
            json={"question": question},
            timeout=2
        )
        if response.ok:
            data = response.json()
            return "\n".join([entry["text"] for entry in data["results"]])
    except Exception:
        return ""
    return ""

# 🧠 Build the system and user prompts
# Replaces placeholders #OS and #MAX in the system prompt
def build_prompt(user_input, max_suggestions, distro):
    is_raw = user_input.startswith("RAW ")
    if is_raw:
        user_input = user_input[4:].strip()
        system_prompt = load_raw_prompt()
        user_prompt = user_input
        return system_prompt, user_prompt, True

    system_prompt = load_system_prompt()
    system_prompt = system_prompt.replace("#OS", DEFAULT_OS).replace("#MAX", str(DEFAULT_MAX_SUGGESTIONS))

    context = get_manai_context(user_input) if USE_MANAI else ""
    user_prefix = load_user_prompt_prefix()
    user_prompt = f"{user_prefix}\n{user_input}"
    if context:
        user_prompt += f"\n\nRelevant information from man pages:\n{context}"
    return system_prompt, user_prompt, False

# 🥹 Extract the JSON array from raw response text
def extract_json_array(raw):
    match = re.search(r"\[.*\]", raw, re.DOTALL)
    if match:
        return match.group(0)
    return raw

# 🤖 Send prompt to the AI model via Ollama and parse the response
def ai_complete(prompt, system_prompt, model, passthrough=False):
    def call_ollama():
        headers = {"Content-Type": "application/json"}
        data = {
            "model": model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
        }
        return requests.post(OLLAMA_API, json=data, headers=headers)

    response = call_ollama()
    if response.ok:
        raw = response.json()["response"].strip()
        if passthrough:
            print(raw)
            return []

        if DEFAULT_DEBUG:
            print("### RAW RESPONSE:\n" + raw + "\n")

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            try:
                fixed = extract_json_array(raw)
                return ast.literal_eval(fixed)
            except:
                pass

        response = call_ollama()
        if response.ok:
            raw = response.json()["response"].strip()
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                try:
                    fixed = extract_json_array(raw)
                    return ast.literal_eval(fixed)
                except:
                    return [f"# Fallback to raw:\n{raw}"]
        else:
            return [f"# Error on retry: {response.status_code}"]
    else:
        return [f"# Error: {response.status_code}"]

# 🚀 Main CLI interface
if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
        max_count = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else DEFAULT_MAX_SUGGESTIONS
        distro = sys.argv[3] if len(sys.argv) > 3 else detect_os()
        model = os.getenv("COMPL_AI_TER_MODEL", DEFAULT_MODEL)

        system_prompt, user_prompt, is_raw = build_prompt(user_input, max_count, distro)
        suggestions = ai_complete(user_prompt, system_prompt, model, passthrough=is_raw)

        for s in suggestions:
            if isinstance(s, dict) and "command" in s:
                print(s["command"])
            else:
                print(s)
    else:
        print("# No input given.")
