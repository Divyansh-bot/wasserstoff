import ollama
import numpy as np
from typing import List

def generate_embedding(text: str) -> np.ndarray:
    try:
        response = ollama.embeddings(model="mistral", prompt=text)
        embedding = response["embedding"]
        return np.array(embedding, dtype=np.float32)
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return np.zeros((384,), dtype=np.float32)  # Fallback shape
