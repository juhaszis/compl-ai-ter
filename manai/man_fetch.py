import os
import subprocess
import requests
from bs4 import BeautifulSoup

MANPAGES_DIR = "manpages"
COMMANDS_FILE = "top_commands.txt"
HEADERS = {"User-Agent": "Mozilla/5.0"}

os.makedirs(MANPAGES_DIR, exist_ok=True)

def save_text(command, content):
    path = os.path.join(MANPAGES_DIR, f"{command}.txt")
    with open(path, "w") as f:
        f.write(content)
    print(f"✅ Saved: {path}")

def generate_man(command):
    try:
        output = subprocess.check_output(["man", "-P", "cat", command], env={"LANG": "C"}, stderr=subprocess.DEVNULL)
        save_text(command, output.decode())
        return True
    except subprocess.CalledProcessError:
        return False

def fetch_man7(command):
    url = f"https://man7.org/linux/man-pages/man1/{command}.1.html"
    print(f"🌐 Trying man7.org: {url}")
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        content = soup.get_text()
        save_text(command, content)
        return True
    return False

def fetch_manpages_org(command):
    url = f"https://manpages.org/{command}"
    print(f"🌐 Trying manpages.org: {url}")
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        content = soup.get_text()
        save_text(command, content)
        return True
    return False

def fetch_command(command):
    if generate_man(command):
        return
    elif fetch_man7(command):
        return
    elif fetch_manpages_org(command):
        return
    else:
        print(f"❌ Failed to get man page for: {command}")

with open(COMMANDS_FILE) as f:
    commands = [line.strip() for line in f.readlines() if line.strip()]

for cmd in commands:
    path = os.path.join(MANPAGES_DIR, f"{cmd}.txt")
    if os.path.exists(path) and os.path.getsize(path) > 0:
        print(f"⏭️  Already exists: {cmd}.txt")
    else:
        print(f"📄 Processing: {cmd}")
        fetch_command(cmd)
