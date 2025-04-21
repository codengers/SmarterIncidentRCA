import chromadb
from chromadb.utils import embedding_functions
import os

client = chromadb.PersistentClient(path=".chromadb")
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
