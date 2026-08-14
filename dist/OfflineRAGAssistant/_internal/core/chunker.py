"""
Handles text splitting and chunking using langchain-text-splitters.
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter


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

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )

    chunked_docs = []

    for doc in docs:
        text = doc.get("text", "")
        source = doc.get("source", "unknown")
        page = doc.get("page", 1)
        doc_type = doc.get("type", "unknown")

        if not text or not text.strip():
            continue

        chunks = splitter.split_text(text)
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
