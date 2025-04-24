import chromadb
from chromadb.utils import embedding_functions
import os

# Try to use persistent client, fallback to in-memory if it fails
try:
    os.makedirs(".chromadb", exist_ok=True)
    client = chromadb.PersistentClient(path=".chromadb")
except Exception as e:
    print(f"[WARNING] Falling back to in-memory ChromaDB: {e}")
    client = chromadb.Client()  # in-memory fallback

collection = client.get_or_create_collection("incident_memory")

embedding_fn = embedding_functions.DefaultEmbeddingFunction()

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
