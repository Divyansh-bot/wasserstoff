# backend/app/services/ocr_service.py

from paddleocr import PaddleOCR
import cv2
import os
from pdf2image import convert_from_path

# Initialize OCR only once
ocr_model = PaddleOCR(use_angle_cls=True, lang='en')

def extract_text_from_image(image_path: str) -> str:
    """Extract text from a single image file."""
    result = ocr_model.ocr(image_path, cls=True)
    extracted_text = ""
    for line in result:
        for word_info in line:
            extracted_text += word_info[1][0] + " "
    return extracted_text.strip()


def extract_text_from_scanned_pdf(pdf_path: str, temp_image_dir="temp_images") -> str:
    """Converts scanned PDF to images and extracts text via OCR."""
    os.makedirs(temp_image_dir, exist_ok=True)
    pages = convert_from_path(pdf_path)
    
    full_text = ""
    for idx, page in enumerate(pages):
        image_path = os.path.join(temp_image_dir, f"page_{idx + 1}.png")
        page.save(image_path, "PNG")
        text = extract_text_from_image(image_path)
        full_text += text + "\n"
        os.remove(image_path)
    
    return full_text.strip()
