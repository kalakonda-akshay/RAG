"""
Handles PDF text extraction using PyMuPDF with automatic OCR fallback for scanned documents.
"""
import os
import shutil
import sys

_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        fitz = None

try:
    from PIL import Image
except ImportError:
    Image = None

try:
    import pytesseract
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
except ImportError:
    pytesseract = None


def _ocr_page_pixmap(page) -> str:
    """
    Renders a PDF page to a high-resolution image and runs OCR via Tesseract.
    """
    if Image is None or pytesseract is None:
        return ""
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

    if fitz is None:
        raise RuntimeError("PyMuPDF (fitz) library is not available. Please install pymupdf.")

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
