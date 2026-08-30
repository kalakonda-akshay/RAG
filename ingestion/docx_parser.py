"""
Handles DOCX text extraction using python-docx.
"""
import os
import sys

_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

try:
    import docx
except ImportError:
    docx = None


def extract_text_from_docx(file_path: str) -> list[dict]:
    """
    Extracts text from a DOCX file, grouping paragraphs into chunks of ~500 words.
    Returns list of dicts: {"text": "<chunk text>", "source": "<filename>", "page": <chunk_index>, "type": "docx"}
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if docx is None:
        raise RuntimeError("python-docx library is not available. Please install python-docx.")

    filename = os.path.basename(file_path)
    doc = docx.Document(file_path)

    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    if not paragraphs:
        return []

    results = []
    current_chunk_paragraphs = []
    current_word_count = 0
    chunk_index = 1

    for para in paragraphs:
        words = para.split()
        word_count = len(words)

        current_chunk_paragraphs.append(para)
        current_word_count += word_count

        if current_word_count >= 500:
            chunk_text = "\n\n".join(current_chunk_paragraphs).strip()
            if chunk_text:
                results.append({
                    "text": chunk_text,
                    "source": filename,
                    "page": chunk_index,
                    "type": "docx"
                })
                chunk_index += 1
            current_chunk_paragraphs = []
            current_word_count = 0

    if current_chunk_paragraphs:
        chunk_text = "\n\n".join(current_chunk_paragraphs).strip()
        if chunk_text:
            results.append({
                "text": chunk_text,
                "source": filename,
                "page": chunk_index,
                "type": "docx"
            })

    return results
