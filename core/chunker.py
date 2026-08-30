"""
Handles text splitting and chunking using langchain-text-splitters.
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
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    RecursiveCharacterTextSplitter = None


def _fallback_split(text: str, chunk_size: int = 300, chunk_overlap: int = 50) -> list[str]:
    words = text.split()
    chunks = []
    i = 0
    step = max(1, chunk_size - chunk_overlap)
    while i < len(words):
        chunk_words = words[i:i + chunk_size]
        chunks.append(" ".join(chunk_words))
        i += step
    return chunks


def chunk_documents(
    docs: list[dict], chunk_size: int = 300, chunk_overlap: int = 50
) -> list[dict]:
    """
    Splits input document text into overlapping chunks while preserving metadata.
    Returns a list of dicts:
    {"text": "<chunk text>", "source": "<filename>", "page": <page>, "type": "<type>", "chunk_id": "<unique id>"}
    """
    if not docs:
        return []

    if RecursiveCharacterTextSplitter is not None:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )
    else:
        splitter = None

    chunked_docs = []

    for doc in docs:
        text = doc.get("text", "")
        source = doc.get("source", "unknown")
        page = doc.get("page", 1)
        doc_type = doc.get("type", "unknown")

        if not text or not text.strip():
            continue

        if splitter is not None:
            chunks = splitter.split_text(text)
        else:
            chunks = _fallback_split(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        for chunk_idx, chunk_text in enumerate(chunks):
            cleaned_text = chunk_text.strip()
            if not cleaned_text:
                continue

            chunk_id = f"{source}_{page}_{chunk_idx}"
            chunked_docs.append({
                "text": cleaned_text,
                "source": source,
                "page": page,
                "type": doc_type,
                "chunk_id": chunk_id,
            })

    return chunked_docs
