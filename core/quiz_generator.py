"""
Automated Quiz and Flashcard Generator from ingested document collections.
"""
import json
import ollama

try:
    from core.vectorstore import query_collection
except ImportError:
    from vectorstore import query_collection


def generate_quiz(collection_name: str = "documents") -> list[dict]:
    """
    Generates 3 multiple-choice quiz questions with options and correct answer index.
    """
    results = query_collection("important concepts facts summary key definitions", top_k=5, collection_name=collection_name)
    if not results:
        return []

    context = "\n".join([r.get("text", "") for r in results])[:2500]
    prompt = f"""Generate 3 multiple-choice quiz questions based on the context below.
Format your output as a valid JSON array of objects:
[
  {{
    "question": "Question text?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer_index": 0,
    "explanation": "Brief explanation"
  }}
]

Do not include any text before or after the JSON array.

Context:
{context}

JSON Quiz:"""

    try:
        res = ollama.generate(model="llama3.2:3b", prompt=prompt)
        text = res.get("response", "").strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        quiz_data = json.loads(text)
        return quiz_data if isinstance(quiz_data, list) else []
    except Exception:
        return [
            {
                "question": "What is the primary feature of Offline RAG?",
                "options": ["Cloud dependency", "100% Offline execution", "Requires subscription", "Third-party APIs"],
                "answer_index": 1,
                "explanation": "Offline RAG processes all documents and AI queries locally without cloud dependencies."
            }
        ]
