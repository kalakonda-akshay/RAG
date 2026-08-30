"""
Offline Multi-Language Translation Engine.
"""
import ollama


LANGUAGES = ["Spanish", "French", "German", "Hindi", "Japanese", "Chinese", "Italian", "Portuguese"]


def translate_text(text: str, target_language: str, model: str = "llama3.2:3b") -> str:
    """
    Translates input text into the target language offline.
    """
    if not text or not text.strip():
        return ""

    prompt = f"""Translate the following text into {target_language}.
Output ONLY the translated text. Do not add any explanation or preamble.

Text:
{text}

Translation in {target_language}:"""

    try:
        res = ollama.generate(model=model, prompt=prompt)
        return res.get("response", "").strip()
    except Exception as e:
        return f"Translation error: {str(e)}"
