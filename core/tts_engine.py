"""
Offline Text-to-Speech (TTS) engine using pyttsx3.
"""
import os
import sys
import tempfile

_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None


def speak_text_to_file(text: str) -> str | None:
    """
    Synthesizes speech from text and saves it as a WAV audio file.
    Returns the absolute path to the generated audio file.
    """
    if not text or not text.strip() or pyttsx3 is None:
        return None

    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 175)  # Speaking speed
        engine.setProperty("volume", 1.0)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            audio_path = tmp_file.name

        engine.save_to_file(text, audio_path)
        engine.runAndWait()
        return audio_path
    except Exception:
        return None
