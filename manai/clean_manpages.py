import os
import re

MANPAGES_DIR = "manpages"

for filename in os.listdir(MANPAGES_DIR):
    filepath = os.path.join(MANPAGES_DIR, filename)
    if filename.endswith(".txt") and os.path.isfile(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace 2+ empty lines with a single empty line
        cleaned = re.sub(r"\n\s*\n+", "\n\n", content)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(cleaned)
        print(f"✅ Cleaned: {filename}")
