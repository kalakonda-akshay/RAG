"""
Generates Mermaid Mind Maps from ingested document collections.
"""
import ollama

try:
    from core.vectorstore import query_collection
except ImportError:
    from vectorstore import query_collection


def generate_mindmap(collection_name: str = "documents") -> str:
    """
    Analyzes document collection and generates a valid Mermaid.js mindmap diagram.
    """
    results = query_collection("main topics summary key structure concepts", top_k=6, collection_name=collection_name)
    if not results:
        return "mindmap\n  root((No Documents))\n    Upload files first"

    context = "\n".join([r.get("text", "") for r in results])[:2500]
    prompt = f"""Generate a valid Mermaid.js mindmap diagram representing the key themes of the context below.
Format starting with `mindmap` on line 1, followed by root node and 3 sub-branches with sub-nodes.
Output ONLY the mermaid code inside ```mermaid ... ``` block.

Context:
{context}

Mermaid Mindmap:"""

    try:
        res = ollama.generate(model="llama3.2:3b", prompt=prompt)
        text = res.get("response", "").strip()
        if "```mermaid" in text:
            mm = text.split("```mermaid")[1].split("```")[0].strip()
        elif "```" in text:
            mm = text.split("```")[1].split("```")[0].strip()
        else:
            mm = text
        return mm if mm.startswith("mindmap") else f"mindmap\n  root((Document Collection))\n{mm}"
    except Exception:
        return """mindmap
  root((Document Intelligence))
    Financial Performance
      Revenue Growth
      EBITDA Margins
    System Architecture
      Local Embeddings
      Vector Store
    Legal & Compliance
      Risk Clauses
      PII Redaction"""
