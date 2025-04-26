# Simple initialization script to fetch, clean, and index manpages for ManAI

import subprocess

def run_step(description, command):
    print(f"\n➡️  {description}...")
    result = subprocess.run(command, shell=True)
    if result.returncode == 0:
        print(f"✅ {description} completed successfully.")
    else:
        print(f"❌ {description} failed!")
        exit(1)

if __name__ == "__main__":
    print("\n🛠️  Initializing ManAI project...")

    # Step 1: Fetch manpages
    run_step("Fetching man pages", "python man_fetch.py")

    # Step 2: Clean manpages
    run_step("Cleaning man pages", "python clean_manpages.py")

    # Step 3: Generate embeddings and build database
    run_step("Generating embeddings and building vector database", "python index_manpages.py")

    print("\n🎉 ManAI initialization completed!")
