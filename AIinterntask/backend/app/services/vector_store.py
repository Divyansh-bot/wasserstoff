# backend/app/services/vector_store.py

import faiss
import numpy as np
import os
import pickle

VECTOR_STORE_PATH = "backend/app/vector_store/index.faiss"
METADATA_STORE_PATH = "backend/app/vector_store/meta.pkl"

class VectorStore:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

        # Load if exists
        if os.path.exists(VECTOR_STORE_PATH) and os.path.exists(METADATA_STORE_PATH):
            faiss.read_index_into(self.index, VECTOR_STORE_PATH)
            with open(METADATA_STORE_PATH, "rb") as f:
                self.metadata = pickle.load(f)

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
        faiss.write_index(self.index, VECTOR_STORE_PATH)
        with open(METADATA_STORE_PATH, "wb") as f:
            pickle.dump(self.metadata, f)
