from typing import List

def split_text_into_chunks(text: str, max_chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    words = text.split()
    chunks = []
    current_chunk = []
    current_len = 0

    for word in words:
        word_len = len(word) + 1  # plus space
        if current_len + word_len <= max_chunk_size:
            current_chunk.append(word)
            current_len += word_len
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = current_chunk[-(overlap // word_len):] if overlap > 0 else []
            current_chunk.append(word)
            current_len = sum(len(w) + 1 for w in current_chunk)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
