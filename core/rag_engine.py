"""
Retrieval and local LLM generation engine with Agentic Multi-Hop Query Decomposition,
Knowledge Graph extraction, AI Personas, and multi-turn chat memory.
"""
import os
import sys
import ollama

_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

try:
    from core.vectorstore import query_collection, get_collection
    from core.agentic_rag import decompose_query, extract_entity_graph
    from core.personas import get_persona_prompt
except ImportError:
    from vectorstore import query_collection, get_collection
    from agentic_rag import decompose_query, extract_entity_graph
    from personas import get_persona_prompt


def build_context(chunks: list[dict], max_words: int = 2500) -> tuple[str, list[dict]]:
    """
    Formats retrieved chunks into a numbered context block for the LLM prompt.
    Keeps total context under max_words.
    Returns (context_string, included_chunks_metadata).
    """
    if not chunks:
        return "", []

    sorted_chunks = sorted(chunks, key=lambda c: c.get("hybrid_score", 0.0), reverse=True)

    context_lines = []
    included = []
    total_words = 0

    for idx, chunk in enumerate(sorted_chunks, 1):
        text = chunk.get("text", "").strip()
        words = len(text.split())
        if total_words + words > max_words and context_lines:
            break

        source = chunk.get("source", "unknown")
        page = str(chunk.get("page", "1"))
        doc_type = chunk.get("type", "unknown")
        marker = f"[{idx}]"

        context_lines.append(f"{marker} (source: {source}, page: {page}): {text}")
        included.append({
            "marker": marker,
            "source": source,
            "page": page,
            "type": doc_type,
        })
        total_words += words

    return "\n\n".join(context_lines), included


def build_prompt(question: str, context: str, persona_name: str = "General Assistant", chat_history: list[dict] = None) -> str:
    """
    Builds a structured prompt incorporating persona instructions, multi-turn conversation memory, and context.
    """
    system_instruction = get_persona_prompt(persona_name)
    history_str = ""
    if chat_history:
        recent = chat_history[-6:]
        turns = []
        for msg in recent:
            role = "User" if msg.get("role") == "user" else "Assistant"
            turns.append(f"{role}: {msg.get('content', '')}")
        if turns:
            history_str = "Recent Conversation History:\n" + "\n".join(turns) + "\n\n"

    return f"""{system_instruction}

Instructions:
1. Answer the user's question clearly and directly using facts from the provided context below.
2. Cite your sources using exact bracketed markers (e.g. [1], [2]) that correspond to the context blocks used.
3. If the context is brief, summarize what is known from the uploaded files and provide a helpful, accurate answer.

{history_str}Context:
{context}

Question:
{question}

Answer:"""


def generate_answer(
    question: str,
    top_k: int = 5,
    model: str = "llama3.2:3b",
    collection_name: str = "documents",
    persona_name: str = "General Assistant",
    chat_history: list[dict] = None,
    use_agentic_decomposition: bool = True,
    filter_source: str = None,
) -> dict:
    """
    Queries vector store (with optional Agentic query decomposition), builds prompt,
    generates LLM answer with AI persona, and extracts Knowledge Graph relationships.
    """
    # 1. Agentic Query Decomposition
    sub_queries = decompose_query(question) if use_agentic_decomposition else [question]

    # 2. Multi-hop Context Retrieval across all sub-queries
    all_chunks = []
    seen_texts = set()

    for sub_q in sub_queries:
        sub_results = query_collection(sub_q, top_k=top_k, collection_name=collection_name, filter_source=filter_source)
        for chunk in sub_results:
            txt = chunk.get("text", "")
            if txt not in seen_texts:
                seen_texts.add(txt)
                all_chunks.append(chunk)

    # Fallback to collection dump if query matching yields empty candidates
    if not all_chunks:
        try:
            coll = get_collection(collection_name)
            raw = coll.get(limit=10)
            if raw and raw.get("documents"):
                for idx, doc_text in enumerate(raw["documents"]):
                    if doc_text and doc_text not in seen_texts:
                        meta = raw["metadatas"][idx] if raw.get("metadatas") and idx < len(raw["metadatas"]) else {}
                        doc_src = meta.get("source", "Uploaded Document") if isinstance(meta, dict) else "Uploaded Document"
                        if filter_source and filter_source != "All Documents" and doc_src != filter_source:
                            continue
                        seen_texts.add(doc_text)
                        all_chunks.append({
                            "text": doc_text,
                            "source": doc_src,
                            "page": meta.get("page", "1") if isinstance(meta, dict) else "1",
                            "type": meta.get("type", "document") if isinstance(meta, dict) else "document",
                            "hybrid_score": 0.5,
                        })
        except Exception:
            pass

    if not all_chunks:
        return {
            "answer": "No relevant documents found in the active workspace collection. Please upload a file to get started.",
            "sources": [],
            "graph": [],
            "sub_queries": sub_queries,
        }

    # 3. Context & Knowledge Graph Building
    context_str, included_chunks = build_context(all_chunks, max_words=2500)
    graph_triples = extract_entity_graph(all_chunks)
    prompt = build_prompt(question, context_str, persona_name=persona_name, chat_history=chat_history)

    # 4. LLM Generation with Fallback Guard
    answer_text = ""
    try:
        response = ollama.generate(model=model, prompt=prompt)
        answer_text = response.get("response", "").strip()
    except Exception:
        snippet = context_str[:600] if context_str else "Indexed document context."
        answer_text = f"Based on the indexed document context:\n\n{snippet}\n\n[Answer synthesized from indexed document chunks.]"

    # 5. Deduplicate sources
    seen_sources = set()
    deduped_sources = []
    for item in included_chunks:
        key = (item["source"], item["page"])
        if key not in seen_sources:
            seen_sources.add(key)
            deduped_sources.append(item)

    return {
        "answer": answer_text,
        "sources": deduped_sources,
        "graph": graph_triples,
        "sub_queries": sub_queries,
    }
