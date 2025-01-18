import chromadb
from chromadb.config import Settings

class ChromaDBClient:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=".chromadb"  # Change as needed
        ))
        self.collection = None

    def set_collection(self, collection_name: str):
        self.collection = self.client.get_or_create_collection(collection_name)

    def add_document(self, document_id: str, text: str, metadata: dict):
        if not self.collection:
            raise ValueError("Collection not set.")
        self.collection.add(documents=[text], ids=[document_id], metadatas=[metadata])

    def query(self, query_text: str, top_k: int = 5):
        if not self.collection:
            raise ValueError("Collection not set.")
        return self.collection.query(query_texts=[query_text], n_results=top_k)
