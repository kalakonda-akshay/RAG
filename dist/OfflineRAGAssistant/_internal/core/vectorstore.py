"""
ChromaDB vector store wrapper for persistent offline indexing and similarity search.
"""
import os
import sys
import chromadb

# Ensure project root is on sys.path for direct script execution
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

try:
    from core.embedder import embed_text, embed_batch
    from core.chunker import chunk_documents
except ImportError:
    from embedder import embed_text, embed_batch
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
    Embeds query_text, queries ChromaDB for top_k nearest chunks, and returns formatted results.
    Returns: list of {"text": ..., "source": ..., "page": ..., "type": ..., "distance": ...}
    """
    collection = get_collection(collection_name)
    count = collection.count()
    if count == 0:
        return []

    query_vector = embed_text(query_text)
    actual_k = min(top_k, count)
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=actual_k,
        include=["documents", "metadatas", "distances"],
    )

    formatted_results = []
    if results and "documents" in results and results["documents"]:
        docs = results["documents"][0]
        metas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for i in range(len(docs)):
            doc_text = docs[i]
            meta = metas[i] if i < len(metas) and metas[i] is not None else {}
            dist = distances[i] if i < len(distances) else 0.0

            formatted_results.append({
                "text": doc_text,
                "source": meta.get("source", ""),
                "page": meta.get("page", ""),
                "type": meta.get("type", ""),
                "distance": dist,
            })

    return formatted_results


if __name__ == "__main__":
    from ingestion.router import process_file

    if len(sys.argv) < 2:
        print("Usage: python core/vectorstore.py <path/to/file>")
        sys.exit(1)

    input_file = sys.argv[1]
    print(f"Processing '{input_file}'...")
    raw_docs = process_file(input_file)
    print(f"Extracted {len(raw_docs)} document sections.")

    chunked = chunk_documents(raw_docs)
    print(f"Created {len(chunked)} chunks.")

    print("Adding chunks to vector store...")
    add_chunks(chunked)
    print("Chunks added successfully.")

    print("\nQuerying collection with 'test query'...")
    search_results = query_collection("test query", top_k=3)
    print(f"Found {len(search_results)} results:")
    for idx, res in enumerate(search_results, 1):
        print(f"\n[{idx}] Source: {res['source']} (Page/Time: {res['page']}, Type: {res['type']}, Distance: {res['distance']:.4f})")
        print(f"    Text: {res['text']}")
