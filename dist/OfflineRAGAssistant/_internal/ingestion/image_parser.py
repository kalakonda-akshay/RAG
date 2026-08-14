"""
Handles OCR text extraction from images using pytesseract and Pillow.
"""
import os
import shutil
from PIL import Image
import pytesseract

# Configure Tesseract binary path on Windows if needed
if os.name == "nt":
    common_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.expanduser(r"~\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"),
    ]
    if not shutil.which("tesseract"):
        for path in common_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                break


def extract_text_from_image(file_path: str) -> list[dict]:
    """
    Extracts text from an image using pytesseract and Pillow.
    Returns a list with one dict: {"text": "<ocr text>", "source": "<filename>", "page": 1, "type": "image"}
    If OCR returns empty/whitespace only, returns an empty list.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    filename = os.path.basename(file_path)

    with Image.open(file_path) as image:
        ocr_text = pytesseract.image_to_string(image).strip()

    if not ocr_text:
        return []

    return [{
        "text": ocr_text,
        "source": filename,
        "page": 1,
        "type": "image"
    }]
