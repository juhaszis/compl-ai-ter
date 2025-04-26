# retrieval_engine.py
# Singleton-style retrieval module for querying manpage chunks from ChromaDB

from sentence_transformers import SentenceTransformer
import chromadb
from config import CHROMA_SETTINGS, CHROMA_COLLECTION, DEBUG, CHROMA_DIR

# Global variables for singleton-like behavior
_model = None        # Embedding model instance
_client = None       # Chroma client instance
_collection = None   # Chroma collection instance

def init():
    if DEBUG:
        print("[DEBUG] Initializing retrieval engine...")
    """
    Initialize embedding model and ChromaDB client only once.
    This ensures efficient resource reuse across multiple queries.
    """
    global _model, _client, _collection

    if _model is None:
        print("🔁 Loading embedding model...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")

    if _client is None:
        _client = chromadb.PersistentClient(CHROMA_DIR)

    if _collection is None:
        _collection = _client.get_collection(CHROMA_COLLECTION)

def query_manpages(question: str, n_results: int = 5):
    """
    Given a natural language question, return the most relevant manpage chunks.

    Args:
        question (str): The user's query.
        n_results (int): Number of top chunks to return (default is 5).

    Returns:
        dict: Result with matching documents and their metadata.
    """
    init()

    if DEBUG:
        print(f"[DEBUG] Querying: '{question}'")

    # Convert the question into an embedding vector
    embedding = _model.encode([question])[0]

    if DEBUG:
        print("[DEBUG] Running ChromaDB query...")

    # Query ChromaDB for top matching chunks
    results = _collection.query(
        query_embeddings=[embedding.tolist()],
        n_results=n_results,
        include=["documents", "metadatas"]
    )
    return results
