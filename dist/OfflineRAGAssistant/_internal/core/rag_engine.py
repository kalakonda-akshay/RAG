"""
Retrieval and local LLM generation engine with source citation support.
"""
import os
import sys
import ollama

# Ensure project root is on sys.path for direct script execution
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

try:
    from core.vectorstore import query_collection
except ImportError:
    from vectorstore import query_collection


def build_context(chunks: list[dict], max_words: int = 2000) -> tuple[str, list[dict]]:
    """
    Formats retrieved chunks into a numbered context block for the LLM prompt.
    Keeps total context under roughly max_words, dropping lower relevance chunks first.
    Returns (context_string, included_chunks_metadata).
    """
    if not chunks:
        return "", []

    # Sort chunks by distance (lowest distance = highest relevance)
    sorted_chunks = sorted(chunks, key=lambda c: c.get("distance", 0.0))

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


def build_prompt(question: str, context: str) -> str:
    """
    Builds a structured prompt instructing the LLM to answer using only the provided context
    and citing sources with [n] markers.
    """
    return f"""You are an accurate, concise, and helpful offline assistant.

Instructions:
1. Answer the user's question ONLY using the facts from the provided context below.
2. If the answer cannot be found in the context, state clearly: "I cannot find the answer in the provided documents." Do not invent or extrapolate information.
3. Always cite your sources using the exact bracketed markers (e.g. [1], [2]) that correspond to the context blocks you used.
4. Keep your answer concise and direct.

Context:
{context}

Question:
{question}

Answer:"""


def generate_answer(question: str, top_k: int = 5, model: str = "llama3.2:3b") -> dict:
    """
    Queries vector store for relevant chunks, builds prompt, and generates LLM answer with source citations.
    Returns:
      {
        "answer": "<LLM's answer text>",
        "sources": [
          {"marker": "[1]", "source": "report.pdf", "page": 3, "type": "pdf"},
          ...
        ]
      }
    """
    chunks = query_collection(question, top_k=top_k)
    if not chunks:
        return {
            "answer": "No relevant information found in the uploaded documents.",
            "sources": [],
        }

    context_str, included_chunks = build_context(chunks, max_words=2000)
    prompt = build_prompt(question, context_str)

    try:
        response = ollama.generate(model=model, prompt=prompt)
        answer_text = response.get("response", "").strip()
    except Exception as e:
        err_msg = str(e).lower()
        if (
            "connection" in err_msg
            or "connect" in err_msg
            or "failed to connect" in err_msg
            or "refused" in err_msg
        ):
            raise ConnectionError(
                "Ollama is not running. Start it with: ollama serve"
            ) from e
        raise

    # Deduplicate sources by (source, page) while preserving first marker and order
    seen = set()
    deduped_sources = []
    for item in included_chunks:
        key = (item["source"], item["page"])
        if key not in seen:
            seen.add(key)
            deduped_sources.append(item)

    return {
        "answer": answer_text,
        "sources": deduped_sources,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        question_input = "What is the main topic of the uploaded documents?"
    else:
        question_input = " ".join(sys.argv[1:])

    print(f"Question: \"{question_input}\"\n")
    try:
        result = generate_answer(question_input)
        print("=== Answer ===")
        print(result["answer"])
        print("\n=== Sources ===")
        if result["sources"]:
            for s in result["sources"]:
                print(f" {s['marker']} {s['source']} (Page/Time: {s['page']}, Type: {s['type']})")
        else:
            print(" None")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
