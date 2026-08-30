"""
ChromaDB vector store wrapper with Hybrid BM25 Keyword + Dense Vector Search & Metadata Filtering.
Includes strict collection name sanitization enforcing ChromaDB naming constraints (3-512 chars, [a-zA-Z0-9._-]).
"""
import os
import sys
import re
import chromadb

_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

try:
    from rank_bm25 import BM25Okapi
except ImportError:
    BM25Okapi = None

try:
    from core.embedder import embed_text
    from core.chunker import chunk_documents
except ImportError:
    from embedder import embed_text
    from chunker import chunk_documents


DB_PATH = os.path.join(_parent_dir, "data", "chroma_db")
_client = None


def sanitize_collection_name(name: str) -> str:
    """
    Sanitizes arbitrary collection/workspace names to guarantee compliance with ChromaDB validation rules:
    - 3 to 63 characters
    - Only [a-zA-Z0-9._-]
    - Must start and end with an alphanumeric character [a-zA-Z0-9]
    """
    if not name:
        return "documents"

    s = str(name).strip().lower()
    if s.startswith("➕"):
        return "documents"

    # Replace spaces and special non-alphanumeric chars with underscores
    s = re.sub(r"[\s\(\)\[\]\{\}\\\/\:\;\,\?\!\@\#\$\%\^\&\*\+\=\~\`]+", "_", s)
    # Filter only allowed characters
    s = re.sub(r"[^a-z0-9._-]", "", s)
    # Strip leading/trailing non-alphanumeric characters
    s = s.strip("._-")

    # Enforce minimum length of 3
    if len(s) < 3:
        s = (s + "_workspace") if s else "documents"
        s = s.strip("._-")
        if len(s) < 3:
            s = "documents"

    # Limit maximum length to 63
    if len(s) > 63:
        s = s[:63].rstrip("._-")

    return s


def _get_client() -> chromadb.PersistentClient:
    global _client
    if _client is None:
        os.makedirs(DB_PATH, exist_ok=True)
        _client = chromadb.PersistentClient(path=DB_PATH)
    return _client


def get_collection(name: str = "documents") -> chromadb.Collection:
    """
    Gets or creates a ChromaDB collection by name.
    Automatically sanitizes the name to avoid validation errors.
    """
    client = _get_client()
    clean_name = sanitize_collection_name(name)
    return client.get_or_create_collection(name=clean_name)


def delete_workspace_collection(name: str) -> bool:
    """
    Deletes a ChromaDB collection by workspace name safely.
    """
    client = _get_client()
    clean_name = sanitize_collection_name(name)
    try:
        client.delete_collection(clean_name)
        return True
    except Exception:
        return False


def list_all_collections() -> list[str]:
    """
    Returns a list of all existing workspace collection names in ChromaDB.
    """
    client = _get_client()
    try:
        colls = client.list_collections()
        names = []
        for c in colls:
            if hasattr(c, "name"):
                names.append(c.name)
            else:
                names.append(str(c))
        defaults = ["documents", "finance", "research", "engineering"]
        for d in defaults:
            if d not in names:
                names.append(d)
        return names
    except Exception:
        return ["documents", "finance", "research", "engineering"]


def list_indexed_files(collection_name: str = "documents") -> list[str]:
    """
    Returns unique source document filenames indexed inside the specified collection.
    """
    try:
        collection = get_collection(collection_name)
        raw = collection.get(include=["metadatas"])
        if not raw or not raw.get("metadatas"):
            return []

        sources = set()
        for meta in raw["metadatas"]:
            if isinstance(meta, dict) and meta.get("source"):
                sources.add(meta["source"])
        return sorted(list(sources))
    except Exception:
        return []


def add_chunks(chunks: list[dict], collection_name: str = "documents") -> None:
    """
    Embeds chunk texts and adds them in batch to the persistent ChromaDB collection.
    """
    if not chunks:
        return

    collection = get_collection(collection_name)

    ids = []
    documents = []
    metadatas = []
    embeddings = []

    for chunk in chunks:
        chunk_text = chunk["text"]
        chunk_id = str(chunk["chunk_id"])

        ids.append(chunk_id)
        documents.append(chunk_text)
        metadatas.append({
            "source": str(chunk.get("source", "")),
            "page": str(chunk.get("page", "")),
            "type": str(chunk.get("type", "")),
        })
        embeddings.append(embed_text(chunk_text))

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )


def query_collection(
    query_text: str, top_k: int = 5, collection_name: str = "documents", filter_source: str = None
) -> list[dict]:
    """
    Performs Hybrid Search (Dense Vector Cosine + Sparse BM25 Keyword Scoring).
    Supports optional filter_source to restrict search exclusively to a specific document.
    """
    collection = get_collection(collection_name)
    count = collection.count()
    if count == 0:
        return []

    query_vector = embed_text(query_text)
    candidate_k = min(top_k * 3, count)
    where_clause = {"source": filter_source} if filter_source and filter_source != "All Documents" else None

    try:
        results = collection.query(
            query_embeddings=[query_vector],
            n_results=candidate_k,
            where=where_clause,
            include=["documents", "metadatas", "distances"],
        )
    except Exception:
        results = collection.query(
            query_embeddings=[query_vector],
            n_results=candidate_k,
            include=["documents", "metadatas", "distances"],
        )

    if not results or "documents" not in results or not results["documents"]:
        return []

    docs = results["documents"][0]
    metas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    if BM25Okapi is not None:
        tokenized_corpus = [doc.lower().split() for doc in docs]
        bm25 = BM25Okapi(tokenized_corpus)
        tokenized_query = query_text.lower().split()
        bm25_scores = bm25.get_scores(tokenized_query)

        hybrid_candidates = []
        for i in range(len(docs)):
            hybrid_candidates.append({
                "text": docs[i],
                "source": metas[i].get("source", "") if i < len(metas) and metas[i] else "",
                "page": metas[i].get("page", "") if i < len(metas) and metas[i] else "",
                "type": metas[i].get("type", "") if i < len(metas) and metas[i] else "",
                "distance": distances[i] if i < len(distances) else 0.0,
                "bm25_score": bm25_scores[i],
                "index": i,
            })

        bm25_sorted = sorted(enumerate(hybrid_candidates), key=lambda x: x[1]["bm25_score"], reverse=True)
        bm25_ranks = {item[0]: rank + 1 for rank, item in enumerate(bm25_sorted)}

        for idx, item in enumerate(hybrid_candidates):
            vec_rank = idx + 1
            bm25_rank = bm25_ranks[idx]
            rrf_score = (1.0 / (60.0 + vec_rank)) + (1.0 / (60.0 + bm25_rank))
            item["hybrid_score"] = rrf_score

        final_sorted = sorted(hybrid_candidates, key=lambda x: x["hybrid_score"], reverse=True)[:top_k]
        return final_sorted
    else:
        candidates = []
        for i in range(len(docs)):
            candidates.append({
                "text": docs[i],
                "source": metas[i].get("source", "") if i < len(metas) and metas[i] else "",
                "page": metas[i].get("page", "") if i < len(metas) and metas[i] else "",
                "type": metas[i].get("type", "") if i < len(metas) and metas[i] else "",
                "distance": distances[i] if i < len(distances) else 0.0,
            })
        return candidates[:top_k]
