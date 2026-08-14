"""
Handles generating embeddings using local Ollama embedding models.
"""
import ollama


def embed_text(text: str, model: str = "nomic-embed-text") -> list[float]:
    """
    Generates an embedding vector for a single string using local Ollama.
    """
    try:
        response = ollama.embeddings(model=model, prompt=text)
        return response["embedding"]
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


def embed_batch(texts: list[str], model: str = "nomic-embed-text") -> list[list[float]]:
    """
    Loops embed_text over a list of texts and returns a list of embedding vectors.
    """
    return [embed_text(text, model=model) for text in texts]
