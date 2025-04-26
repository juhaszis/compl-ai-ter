# 🧠 ManAI - Man Page Retrieval Engine

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20DB-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-WIP-orange)

This project is an offline search engine for Linux manpages that:
- Fetches, cleans, splits, and embeds manpages
- Stores them in ChromaDB
- Allows querying via a Flask API using natural language

---

## 📦 Requirements

- Python 3.10+
- Internet connection (for fetching manpages)
- Installed `man` command on your system
- (Optional) CUDA-enabled GPU for acceleration

Install required Python packages:

```bash
pip install -r requirements.txt
```

---

## 🔥 Preparation

You can initialize everything automatically with a single command:

```bash
python 01_init_manai.py
```

This script will:
- Fetch man pages
- Clean man pages
- Generate embeddings and build the vector database

You can freely edit the `top_commands.txt` file to customize the list of commands whose manpages are processed. After editing, simply rerun the initialization or the individual steps.

Or you can do it step-by-step as detailed below.

---

## 🔥 Preparation Steps

### 1. Fetch man pages

```bash
python man_fetch.py
```
- First tries the local `man` command.
- If unavailable, fetches from online sources (`man7.org`, `manpages.org`).
- Result: `.txt` files in the `manpages/` folder.

---

### 2. Clean man pages

```bash
python clean_manpages.py
```
- Removes multiple empty lines for consistent formatting.

---

### 3. Generate embeddings and build the vector database

```bash
python index_manpages.py
```
- Splitter: `RecursiveCharacterTextSplitter`
- Embedding model: `all-MiniLM-L6-v2`
- Vector database: ChromaDB (stored in `./chroma_store`)

---

## 🚀 Start the API Server

Start the Flask API server:

```bash
python manai_server.py
```

### API Endpoint

- **POST /query**
- Example body:

```json
{
  "question": "how to create a directory?"
}
```

- Example response:

```json
{
  "results": [
    {
      "text": "mkdir - create a directory",
      "file": "mkdir.txt",
      "chunk_index": 0
    },
    ...
  ]
}
```

---

## ⚙️ Configuration

Settings are in `config.py`:

| Parameter | Description |
|-----------|-------------|
| `MANPAGE_DIR` | Directory for manpage text files |
| `CHROMA_DIR` | ChromaDB storage directory |
| `CHROMA_COLLECTION` | ChromaDB collection name |
| `EMBEDDING_MODEL` | Name of the embedding model |
| `CHUNK_SIZE` | Chunk size (characters) |
| `CHUNK_OVERLAP` | Overlap between chunks |
| `SERVER_HOST` | Flask server host address |
| `SERVER_PORT` | Flask server port number |
| `DEBUG` | Debug mode toggle |

---

## 🧪 Quick Test from Terminal

Simple Python script to query the API:

```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={"question": "how to delete a file?"}
)

print(response.json())
```

---

## 📂 Project Structure

```
man_fetch.py         # Fetch manpages
clean_manpages.py    # Clean manpages
index_manpages.py    # Generate embeddings + build ChromaDB
manai_server.py      # Flask API server
retrieval_engine.py  # Query engine module
config.py            # Configuration settings
requirements.txt     # Required packages
top_commands.txt     # List of commands
manpages/            # Downloaded manpage files
chroma_store/        # ChromaDB storage
```

---

## 💬 Notes

- **First run**: It's recommended to run the full pipeline (fetch → clean → index).
- **Adding new commands**: Simply update `top_commands.txt`, fetch and index the new files.
- **Production deployment**: It's recommended to use `gunicorn` or `uvicorn` instead of Flask's development server.

---

# 🎯 Have fun building your own offline Linux manpage retriever!
