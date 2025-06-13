import requests
from app.embeddings.mistral_embedder import generate_embedding
from app.chunking.text_splitter import split_text_into_chunks
from app.vector_store.vector_store import VectorStore
from app.utils.clean_text import clean_and_trim_text

# Instantiate vector DB with embedding dimension
VECTOR_DIM = 4096
store = VectorStore(dim=VECTOR_DIM)

def embed_and_store_text(extracted_text: str, source_name: str):
    cleaned_text = clean_and_trim_text(extracted_text)
    chunks = split_text_into_chunks(cleaned_text)

    for chunk in chunks:
        try:
            embedding = generate_embedding(chunk)
            store.add(embedding.tolist(), {"chunk": chunk, "source": source_name})
        except Exception as e:
            print(f"[❌ ERROR] Failed to embed/store chunk: {chunk[:50]}... -> {e}")

def query_ollama_and_rank(query: str, source_name: str) -> str:
    try:
        query_embedding = generate_embedding(query)
        similar_chunks = store.search(query_embedding.tolist(), top_k=5)

        if not similar_chunks:
            return "No relevant content found in uploaded documents."

        context = "\n".join([chunk["chunk"] for chunk in similar_chunks if chunk.get("source") == source_name])
        prompt = f"""Answer the question based on the context below.
If the question can't be answered using the information, respond with \"I don't know\".

Context:
{context}

Question: {query}
Answer:"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False}
        )

        if response.ok:
            return response.json().get("response", "I don't know.")
        else:
            print(f"[❌ Ollama Error] Status: {response.status_code}, Body: {response.text}")
            return "Ollama model failed to respond."

    except Exception as e:
        print(f"[❌ ERROR] Failed to process query: {e}")
        return "An error occurred while processing your question."
