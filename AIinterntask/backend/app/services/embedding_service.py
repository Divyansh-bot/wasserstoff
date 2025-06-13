# backend/app/services/embedding_service.py

from ollama import Client

# Connect to the running Ollama server
client = Client(host='http://localhost:11434')

def generate_embedding(text: str) -> list:
    """
    Generate embeddings using the Mistral model locally via Ollama.
    """
    try:
        response = client.embeddings(model='mistral', prompt=text)
        return response['embedding']
    except Exception as e:
        print(f"[ERROR] Failed to generate embedding: {e}")
        return []
