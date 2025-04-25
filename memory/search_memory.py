import os
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings

embedding_fn = embedding_functions.DefaultEmbeddingFunction()

try:
    # Try to initialize persistent client
    os.makedirs(".chromadb", exist_ok=True)
    settings = Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=".chromadb"
    )
    client = chromadb.Client(settings)
    print("[ChromaDB] Persistent mode initialized.")
except Exception as e:
    # Fallback for environments like Streamlit Cloud
    print(f"[ChromaDB Warning] Persistent mode failed: {e}")
    client = chromadb.Client()
    print("[ChromaDB] Switched to in-memory mode.")

collection = client.get_or_create_collection("incident_memory")

# Used to retrieve top-N similar past incidents
def get_similar_incidents(incident, top_k=3):
    query_text = f"{incident['short_description']} {incident['description']}"
    results = collection.query(query_texts=[query_text], n_results=top_k)
    if not results["documents"]:
        return "No similar incidents found."
    output = ""
    for doc in results["documents"][0]:
        output += f"- {doc}\n"
    return output
