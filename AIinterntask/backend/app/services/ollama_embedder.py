# backend/app/services/ollama_embedder.py

import requests

def generate_embeddings(text_chunks):
    embeddings = []
    for chunk in text_chunks:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": f"Generate a concise vector-like semantic representation of this chunk:\n\n{chunk}",
                "stream": False
            }
        )
        try:
            result = response.json()["response"].strip()
            embeddings.append(result)
        except:
            embeddings.append("")  # fallback if anything fails
    return embeddings
