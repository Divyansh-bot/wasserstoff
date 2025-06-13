import faiss
import numpy as np
import os
import pickle
from typing import List, Tuple

FAISS_INDEX_PATH = "data/faiss_index.index"
METADATA_PATH = "data/metadata.pkl"

def save_faiss_index(index: faiss.IndexFlatL2, path: str = FAISS_INDEX_PATH) -> None:
    faiss.write_index(index, path)

def load_faiss_index(path: str = FAISS_INDEX_PATH) -> faiss.IndexFlatL2:
    if not os.path.exists(path):
        raise FileNotFoundError(f"FAISS index not found at: {path}")
    return faiss.read_index(path)

def save_metadata(metadata: List[str], path: str = METADATA_PATH) -> None:
    with open(path, 'wb') as f:
        pickle.dump(metadata, f)

def load_metadata(path: str = METADATA_PATH) -> List[str]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Metadata not found at: {path}")
    with open(path, 'rb') as f:
        return pickle.load(f)

def create_faiss_index(embeddings: List[np.ndarray]) -> faiss.IndexFlatL2:
    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype('float32'))
    return index

def search_index(index: faiss.IndexFlatL2, query_vector: np.ndarray, top_k: int = 5) -> Tuple[np.ndarray, np.ndarray]:
    query_vector = np.array([query_vector]).astype('float32')
    distances, indices = index.search(query_vector, top_k)
    return distances[0], indices[0]
