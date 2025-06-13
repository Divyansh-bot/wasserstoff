import os
import fitz  # PyMuPDF
import pdfplumber
from docx import Document
from paddleocr import PaddleOCR
import pytesseract
import io
import numpy as np
import cv2
from PIL import Image

ocr_pipeline = PaddleOCR(use_angle_cls=True, lang='en')

def extract_text_from_pdf(path: str) -> str:
    try:
        with pdfplumber.open(path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() or ''
            return text.strip()
    except Exception:
        try:
            # Fallback to OCR if PDF is image-based
            doc = fitz.open(path)
            images = [page.get_pixmap().pil_tobytes("jpeg") for page in doc]
            return extract_text_from_images(images)
        except Exception as e:
            return f"[PDF Extraction Failed] {str(e)}"

def extract_text_from_docx(path: str) -> str:
    try:
        doc = Document(path)
        return '\n'.join([para.text for para in doc.paragraphs]).strip()
    except Exception as e:
        return f"[DOCX Extraction Failed] {str(e)}"

def extract_text_from_image(path: str) -> str:
    try:
        img = cv2.imread(path)
        result = ocr_pipeline.ocr(img, cls=True)
        text = ""
        for line in result:
            for _, (_, txt) in enumerate(line):
                text += txt[0] + " "
        return text.strip()
    except Exception as e:
        return f"[Image OCR Failed] {str(e)}"

def extract_text_from_images(image_bytes_list) -> str:
    try:
        text = ""
        for img_bytes in image_bytes_list:
            img = Image.open(io.BytesIO(img_bytes))
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            result = ocr_pipeline.ocr(img_cv, cls=True)
            for line in result:
                for _, (_, txt) in enumerate(line):
                    text += txt[0] + " "
        return text.strip()
    except Exception as e:
        return f"[Batch Image OCR Failed] {str(e)}"

def extract_text_from_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(path)
    elif ext == '.docx':
        return extract_text_from_docx(path)
    elif ext in ['.jpg', '.jpeg', '.png']:
        return extract_text_from_image(path)
    else:
        return f"[Unsupported file type: {ext}]"
