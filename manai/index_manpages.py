# update_index.py
# This script updates a Chroma vector store with manpage chunks.
# It only re-embeds files that are new or have changed since the last indexing.

import os
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb

from config import CHROMA_DIR, CHROMA_COLLECTION, MANPAGE_DIR, CHROMA_SETTINGS, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL

# Initialize or load the Chroma vector DB (with persistence)
client = chromadb.PersistentClient(CHROMA_DIR)
collection = client.get_or_create_collection(CHROMA_COLLECTION)

# Load the embedding model
model = SentenceTransformer(EMBEDDING_MODEL)

# Text splitter for chunking documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

# Helper function to extract basic metadata from a file
def get_metadata(filepath):
    stat = os.stat(filepath)
    return {
        "name": os.path.basename(filepath),   # file name
        "size": stat.st_size,                # file size in bytes
        "mtime": int(stat.st_mtime)          # last modified timestamp (epoch)
    }

# Loop through each manpage file in the directory
for filename in os.listdir(MANPAGE_DIR):
    if not filename.endswith(".txt"):
        continue  # skip non-text files

    path = os.path.join(MANPAGE_DIR, filename)
    meta = get_metadata(path)
    doc_id_prefix = filename.replace(".txt", "")

    # Check if this document (chunk 0) already exists in the collection
    existing = collection.get(
        where={"name": meta["name"]},
        include=["metadatas"]
    )

    needs_update = False

    # Decide if the document needs to be indexed
    if not existing["metadatas"]:
        # No entry found → new file
        needs_update = True
    else:
        # Entry exists, check if metadata changed
        old_meta = existing["metadatas"][0]
        if any([
            str(old_meta.get("size")) != str(meta["size"]),
            str(old_meta.get("mtime")) != str(meta["mtime"])
        ]):
            needs_update = True
            collection.delete(where={"name": meta["name"]})  # remove old chunks

    if needs_update:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        chunks = text_splitter.create_documents([content])
        print(f"🔄 Indexing: {filename} ({len(chunks)} chunks)")

        for i, chunk in enumerate(chunks):
            embedding = model.encode(chunk.page_content)
            collection.add(
                documents=[chunk.page_content],
                embeddings=[embedding.tolist()],
                metadatas=[{
                    "name": meta["name"],
                    "size": meta["size"],
                    "mtime": meta["mtime"],
                    "chunk_index": i
                }],
                ids=[f"{doc_id_prefix}-{i}"]
            )
    else:
        print(f"✅ Up-to-date: {filename}")
