"""
Handles plain text, markdown, code, and structured JSON/HTML file ingestion.
"""
import os


def extract_text_from_textfile(file_path: str) -> list[dict]:
    """
    Parses plain text, code, markdown, JSON, or HTML files.
    Returns a list of dicts: {"text": "<content>", "source": "<filename>", "page": 1, "type": "<ext>"}
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    filename = os.path.basename(file_path)
    _, ext = os.path.splitext(file_path)
    ext_clean = ext.lower().lstrip(".")

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read().strip()

    if not content:
        return []

    return [{
        "text": content,
        "source": filename,
        "page": 1,
        "type": ext_clean or "text",
    }]
