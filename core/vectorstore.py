"""
ChromaDB vector store wrapper with Hybrid BM25 Keyword + Dense Vector Search.
"""
import os
import sys
import chromadb
from rank_bm25 import BM25Okapi

_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

try:
    from core.embedder import embed_text
    from core.chunker import chunk_documents
except ImportError:
    from embedder import embed_text
    from chunker import chunk_documents


DB_PATH = os.path.join(_parent_dir, "data", "chroma_db")
_client = None


def _get_client() -> chromadb.PersistentClient:
    global _client
    if _client is None:
        os.makedirs(DB_PATH, exist_ok=True)
        _client = chromadb.PersistentClient(path=DB_PATH)
    return _client


def get_collection(name: str = "documents") -> chromadb.Collection:
    """
    Gets or creates a ChromaDB collection by name.
    """
    client = _get_client()
    return client.get_or_create_collection(name=name)


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
    query_text: str, top_k: int = 5, collection_name: str = "documents"
) -> list[dict]:
    """
    Performs Hybrid Search (Dense Vector Cosine + Sparse BM25 Keyword Scoring)
    to achieve maximum precision on technical terms, acronyms, and semantic queries.
    """
    collection = get_collection(collection_name)
    count = collection.count()
    if count == 0:
        return []

    query_vector = embed_text(query_text)

    # Retrieve candidate pool for hybrid reranking
    candidate_k = min(top_k * 3, count)
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

    # Initialize BM25 over the candidate pool
    tokenized_corpus = [doc.lower().split() for doc in docs]
    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query = query_text.lower().split()
    bm25_scores = bm25.get_scores(tokenized_query)

    # Normalize scores and perform Reciprocal Rank Fusion (RRF)
    hybrid_candidates = []
    for i in range(len(docs)):
        vec_rank = i + 1
        bm25_score = bm25_scores[i]
        
        # RRF formula: Score = 1 / (60 + vector_rank) + 1 / (60 + bm25_rank)
        hybrid_candidates.append({
            "text": docs[i],
            "source": metas[i].get("source", "") if i < len(metas) and metas[i] else "",
            "page": metas[i].get("page", "") if i < len(metas) and metas[i] else "",
            "type": metas[i].get("type", "") if i < len(metas) and metas[i] else "",
            "distance": distances[i] if i < len(distances) else 0.0,
            "bm25_score": bm25_score,
            "index": i,
        })

    # Sort candidates by BM25 score descending to calculate rank
    bm25_sorted = sorted(enumerate(hybrid_candidates), key=lambda x: x[1]["bm25_score"], reverse=True)
    bm25_ranks = {item[0]: rank + 1 for rank, item in enumerate(bm25_sorted)}

    for idx, item in enumerate(hybrid_candidates):
        vec_rank = idx + 1
        bm25_rank = bm25_ranks[idx]
        rrf_score = (1.0 / (60.0 + vec_rank)) + (1.0 / (60.0 + bm25_rank))
        item["hybrid_score"] = rrf_score

    # Sort final top_k by hybrid score descending
    final_sorted = sorted(hybrid_candidates, key=lambda x: x["hybrid_score"], reverse=True)[:top_k]
    return final_sorted
