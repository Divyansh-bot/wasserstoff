# app/utils/similarity.py

import numpy as np
from typing import List

def compute_cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    if a_norm == 0.0 or b_norm == 0.0:
        return 0.0
    return np.dot(a, b) / (a_norm * b_norm)

def compute_similarity_scores(query_embedding: np.ndarray, embeddings: List[np.ndarray]) -> List[float]:
    return [compute_cosine_similarity(query_embedding, emb) for emb in embeddings]
