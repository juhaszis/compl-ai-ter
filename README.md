## 🧠 Terminal AI Shell Completer

> **Disclaimer:**
>
> This is a fun experimental project, so some hardcoded absolute paths may exist. 🚧  
> Performance is strictly tied to the LLM model you choose.  
> The developer is not responsible for any unexpected behavior or catastrophic typing disasters.  
> You have been warned. ⚡

This tool provides intelligent shell command completions using a local LLM via Ollama.

I already had a local AI setup running, so I figured — why not use it like a smart version of the TAB key? This is just a fun little experiment for me, nothing serious — but it's surprisingly useful. It can also enhance answers with relevant man page content, making it ideal for both beginners and power users.

### ✨ Features
- Local shell command completion using Ollama models (e.g. `codellama:13b`)
- Optional contextual augmentation from man pages via the [`manai`](./manai/README.md) service (already included in the `./manai` subdirectory)
- JSON-based output with retry and fallback handling
- RAW mode for general-purpose questions or direct instructions (like a smart encyclopedia)

---

### 💻 CLI Usage
```bash
python3 complaiter.py "cat /var/log/*.log | find all critical error in logs"
```

Example output:
```
1. grep -Ei 'critical.*error|error.*critical' /var/log/*.log
2. find /var/log -name '*.log' -exec grep -Ei 'critical.*error|error.*critical' {} +
3. awk '/[Cc]ritical/ && /[Ee]rror/' /var/log/*.log
```

For general LLM queries (RAW mode):
```bash
python3 complaiter.py "RAW what is the difference between grep and awk"
```

---

### ⚙️ Bash Integration (`.ai-comp`)
To enable shell integration, source your `.ai-comp` helper script from your shell configuration (e.g., `~/.bashrc`, `~/.zshrc`, etc.):

```bash
. /path/to/.ai-comp
```

(Replace `/path/to/` with the actual location where you placed the `.ai-comp` file.)

Once loaded:
- **Alt+A** → Generate 5 AI command suggestions based on the current input line
- **Alt+1..5** → Insert the selected suggestion
- **Alt+S** → RAW query: sends prompt directly and prints the full raw result

---

### 🌐 Environment Variables
| Variable                           | Description                                          | Default                                   |
|------------------------------------|------------------------------------------------------|-------------------------------------------|
| `COMPL_AI_TER_MODEL`              | Model name (Ollama)                                 | `codellama:13b`                           |
| `COMPL_AI_TER_MAX`                | Max number of suggestions                           | `3`                                       |
| `COMPL_AI_TER_USE_MANAI`          | Use man page context enrichment                     | `1`                                       |
| `COMPL_AI_TER_DEBUG`              | Print debug info                                    | `0`                                       |
| `COMPL_AI_TER_PROMPT`             | System prompt file path                             | `~/.se/system_prompt.txt`                 |
| `COMPL_AI_TER_SYSTEM_PROMPT_RAW`  | RAW mode system prompt file                         | `~/.se/system_prompt_raw.txt`             |
| `COMPL_AI_TER_USER_PROMPT_PREFIX` | User prompt prefix file                             | `~/.se/user_prompt_prefix.txt`            |
| `COMPL_AI_TER_MANAI_API`          | Manai API URL                                       | `http://localhost:8000/query`             |

---

### 📦 requirements.txt
```
requests>=2.25
```

---

**In a world of clicks and windows, the terminal stands alone — powerful, precise, yours.**

**Happy hacking!** 💻😎
