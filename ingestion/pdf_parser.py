"""
Handles PDF text extraction using PyMuPDF.
"""
import os
import pymupdf as fitz


def extract_text_from_pdf(file_path: str) -> list[dict]:
    """
    Extracts text from a PDF file page by page using PyMuPDF.
    Returns a list of dicts: {"text": "<page text>", "source": "<filename>", "page": <page_number>, "type": "pdf"}
    Skips pages with no extractable text.
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
            if text:
                results.append({
                    "text": text,
                    "source": filename,
                    "page": page_num + 1,
                    "type": "pdf"
                })
    finally:
        doc.close()

    return results
