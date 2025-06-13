# backend/app/vector_store/vector_store.py

import faiss
import numpy as np
import os
import pickle

VECTOR_STORE_PATH = "backend/app/vector_store/index.faiss"
METADATA_STORE_PATH = "backend/app/vector_store/meta.pkl"

# Ensure the folder exists
os.makedirs(os.path.dirname(VECTOR_STORE_PATH), exist_ok=True)

class VectorStore:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

        if os.path.exists(VECTOR_STORE_PATH) and os.path.exists(METADATA_STORE_PATH):
            try:
                self.index = faiss.read_index(VECTOR_STORE_PATH)
                with open(METADATA_STORE_PATH, "rb") as f:
                    self.metadata = pickle.load(f)
            except Exception as e:
                print(f"[❌ ERROR] Failed to load existing vector store: {e}")

    def add(self, embedding: list, meta: dict):
        vector = np.array([embedding], dtype='float32')
        self.index.add(vector)
        self.metadata.append(meta)
        self._save()

    def search(self, query_vector: list, top_k: int = 5):
        query = np.array([query_vector], dtype='float32')
        distances, indices = self.index.search(query, top_k)
        results = [self.metadata[i] for i in indices[0] if i < len(self.metadata)]
        return results

    def _save(self):
        try:
            os.makedirs(os.path.dirname(VECTOR_STORE_PATH), exist_ok=True)
            faiss.write_index(self.index, VECTOR_STORE_PATH)
            with open(METADATA_STORE_PATH, "wb") as f:
                pickle.dump(self.metadata, f)
        except Exception as e:
            print(f"[❌ ERROR] Saving vector store failed: {e}")
