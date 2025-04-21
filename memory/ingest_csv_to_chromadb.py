import csv
import chromadb
from chromadb.utils import embedding_functions

client = chromadb.PersistentClient(path=".chromadb")
collection = client.get_or_create_collection("incident_memory")
embedding_fn = embedding_functions.DefaultEmbeddingFunction()

with open("incident_data.csv", "r") as file:
    reader = csv.DictReader(file)
    for i, row in enumerate(reader):
        incident_text = f"{row['short_description']} {row['description']}"
        collection.add(
            documents=[incident_text],
            ids=[f"incident_{i}"],
            metadatas=[{"id": row["incident_id"]}]
        )