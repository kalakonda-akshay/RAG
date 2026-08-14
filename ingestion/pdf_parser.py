"""
Handles PDF text extraction using PyMuPDF with automatic OCR fallback for scanned documents.
"""
import os
import shutil
import pymupdf as fitz
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


def _ocr_page_pixmap(page: fitz.Page) -> str:
    """
    Renders a PDF page to a high-resolution image and runs OCR via Tesseract.
    """
    try:
        pix = page.get_pixmap(dpi=150)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        ocr_text = pytesseract.image_to_string(img).strip()
        return ocr_text
    except Exception:
        return ""


def extract_text_from_pdf(file_path: str) -> list[dict]:
    """
    Extracts text from a PDF file page by page.
    Automatically applies OCR on scanned/image-only pages.
    Returns a list of dicts: {"text": "<page text>", "source": "<filename>", "page": <page_number>, "type": "pdf"}
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    filename = os.path.basename(file_path)
    results = []

    doc = fitz.open(file_path)
    try:
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text().strip()

            # If no embedded text found, perform OCR fallback for scanned PDF page
            doc_type = "pdf"
            if not text:
                text = _ocr_page_pixmap(page)
                if text:
                    doc_type = "pdf (scanned)"

            if text:
                results.append({
                    "text": text,
                    "source": filename,
                    "page": page_num + 1,
                    "type": doc_type,
                })
    finally:
        doc.close()

    return results
