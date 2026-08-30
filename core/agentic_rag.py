"""
Agentic Multi-Hop Query Decomposition and Knowledge Graph Entity Extractor.
"""
import os
import sys
import re
import ollama

_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

try:
    from core.vectorstore import query_collection
except ImportError:
    from vectorstore import query_collection


def decompose_query(query: str) -> list[str]:
    """
    Decomposes complex multi-part user queries into targeted sub-queries.
    """
    query_clean = query.strip()
    # Check for conjunctions or compound statements
    if any(k in query_clean.lower() for k in [" and ", " as well as ", " versus ", " compare ", " compared to ", " also "]):
        try:
            prompt = f"Break down the following complex question into 2 or 3 simpler sub-questions for document retrieval. Output only one sub-question per line.\n\nQuestion: {query_clean}\n\nSub-questions:"
            res = ollama.generate(model="llama3.2:3b", prompt=prompt)
            lines = [line.strip("- 123456789.") for line in res.get("response", "").split("\n") if line.strip()]
            if lines:
                return lines[:3]
        except Exception:
            pass

    return [query_clean]


def extract_entity_graph(chunks: list[dict]) -> list[dict]:
    """
    Extracts key entity-relationship triples from retrieved document chunks to construct a Knowledge Graph summary.
    Returns a list of dicts: {"entity_a": ..., "relation": ..., "entity_b": ...}
    """
    if not chunks:
        return []

    combined_text = " ".join([c.get("text", "")[:300] for c in chunks[:3]])
    prompt = f"""Extract key entity relationships from the text below.
Format each line as: Entity A -> Relationship -> Entity B
Do not include any intro or outro. Max 5 lines.

Text:
{combined_text}

Relationships:"""

    try:
        res = ollama.generate(model="llama3.2:3b", prompt=prompt)
        raw_lines = res.get("response", "").split("\n")
        graph_nodes = []
        for line in raw_lines:
            if "->" in line:
                parts = [p.strip() for p in line.split("->")]
                if len(parts) == 3:
                    graph_nodes.append({
                        "source": parts[0],
                        "relation": parts[1],
                        "target": parts[2],
                    })
        return graph_nodes
    except Exception:
        return []
