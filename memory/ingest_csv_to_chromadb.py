import csv
import os
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings

embedding_fn = embedding_functions.DefaultEmbeddingFunction()

# Try persistent client first, fallback to in-memory if needed
try:
    os.makedirs(".chromadb", exist_ok=True)
    settings = Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=".chromadb"
    )
    client = chromadb.Client(settings)
    print("[ChromaDB] Persistent mode initialized.")
except Exception as e:
    print(f"[ChromaDB Warning] Persistent mode failed: {e}")
    client = chromadb.Client()
    print("[ChromaDB] Switched to in-memory mode.")

collection = client.get_or_create_collection("incident_memory")

# Ingest CSV rows as documents into ChromaDB
with open("incident_data.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for i, row in enumerate(reader):
        incident_text = f"{row['short_description']} {row['description']}"
        try:
            collection.add(
                documents=[incident_text],
                ids=[f"incident_{i}"],
                metadatas=[{"id": row["incident_id"]}]
            )
        except Exception as e:
            print(f"Error adding row {i}: {e}")
