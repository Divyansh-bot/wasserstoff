# backend/app/services/pdf_parser.py

import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from all pages of a PDF."""
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"[ERROR] Failed to parse PDF: {e}")
        return ""
    return text.strip()
