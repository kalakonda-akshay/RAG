"""
Handles generating embeddings using local Ollama embedding models with deterministic fallback.
"""
import os
import sys
import hashlib

_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

try:
    import ollama
except ImportError:
    ollama = None


def embed_text(text: str, model: str = "nomic-embed-text") -> list[float]:
    """
    Generates a 768-dim embedding vector using local Ollama if running,
    or a deterministic hash-based 768-dim vector fallback.
    """
    if ollama is not None:
        try:
            response = ollama.embeddings(model=model, prompt=text)
            if response and "embedding" in response:
                return response["embedding"]
        except Exception:
            pass

    # Deterministic 768-dimensional fallback embedding
    words = text.lower().split()
    vec = [0.0] * 768
    for idx, w in enumerate(words):
        h = int(hashlib.md5(w.encode("utf-8", errors="ignore")).hexdigest(), 16)
        slot = h % 768
        vec[slot] += 1.0 / (idx + 1)

    norm = sum(v * v for v in vec) ** 0.5 or 1.0
    return [v / norm for v in vec]


def embed_batch(texts: list[str], model: str = "nomic-embed-text") -> list[list[float]]:
    """
    Loops embed_text over a list of texts and returns a list of embedding vectors.
    """
    return [embed_text(text, model=model) for text in texts]
