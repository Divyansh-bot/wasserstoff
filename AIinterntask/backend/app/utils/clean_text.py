import re

def clean_and_trim_text(text: str) -> str:
    """
    Removes extra spaces, newlines, and special characters.
    Keeps only clean text for embedding and chunking.
    """
    # Remove extra whitespace and line breaks
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = re.sub(r'\s+', ' ', text)

    # Optionally: remove non-ASCII or special chars
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    return text.strip()
