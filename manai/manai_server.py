# manai_server.py
# Flask-based API server for querying manpage chunks using ChromaDB + SentenceTransformer

from flask import Flask, request, jsonify
from retrieval_engine import query_manpages

# Create a Flask app instance
app = Flask(__name__)

# Define a route to handle POST requests for querying manpages
@app.route("/query", methods=["POST"])
def query():
    # Extract JSON data from the incoming request
    data = request.json
    question = data.get("question", "").strip()

    # Validate input
    if not question:
        return jsonify({"error": "Missing 'question' in request."}), 400

    try:
        # Use the retrieval engine to get top matching chunks
        results = query_manpages(question)
        output = []

        # Format each result with text and metadata
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            output.append({
                "text": doc.strip(),               # Chunk content
                "file": meta.get("name"),         # Source file name
                "chunk_index": meta.get("chunk_index")  # Chunk number in that file
            })

        # Return the structured results
        return jsonify({"results": output})

    except Exception as e:
        # Return any error that occurs during processing
        return jsonify({"error": str(e)}), 500

# Entry point to run the Flask development server
if __name__ == "__main__":
    from config import SERVER_HOST, SERVER_PORT
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)
