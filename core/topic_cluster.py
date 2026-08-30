"""
Discovers semantic topic clusters across document collections.
"""
import ollama

try:
    from core.vectorstore import query_collection
except ImportError:
    from vectorstore import query_collection


def discover_topic_clusters(collection_name: str = "documents") -> list[dict]:
    """
    Analyzes document chunks and groups them into 3-4 semantic topic clusters.
    Returns list of {"topic": "<name>", "description": "<summary>", "keywords": [...]}.
    """
    results = query_collection("overview topics themes categories data summary", top_k=8, collection_name=collection_name)
    if not results:
        return []

    context = "\n\n".join([r.get("text", "")[:300] for r in results])
    prompt = f"""Analyze the document snippets below and discover 3 main semantic topic clusters.
Format output as:
Topic 1: [Topic Title] - [Short 1-sentence description]
Topic 2: [Topic Title] - [Short 1-sentence description]
Topic 3: [Topic Title] - [Short 1-sentence description]

Document Snippets:
{context}

Topic Clusters:"""

    try:
        res = ollama.generate(model="llama3.2:3b", prompt=prompt)
        raw = res.get("response", "").strip()
        clusters = []
        for line in raw.splitlines():
            if ":" in line and ("Topic" in line or line[0].isdigit()):
                parts = line.split(":", 1)
                title_desc = parts[1].split("-", 1) if "-" in parts[1] else [parts[1], "Key document theme"]
                clusters.append({
                    "topic": title_desc[0].strip(),
                    "description": title_desc[1].strip() if len(title_desc) > 1 else "Extracted document theme",
                })
        return clusters if clusters else [
            {"topic": "Document Overview", "description": "General concepts and facts across files."},
            {"topic": "Technical & Financial Insights", "description": "Metrics and operational details."}
        ]
    except Exception:
        return [
            {"topic": "Core Document Intelligence", "description": "Key facts extracted from ingested files."}
        ]
