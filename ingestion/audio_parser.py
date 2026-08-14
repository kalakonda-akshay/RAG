"""
Handles audio transcription using faster-whisper.
"""
import os
from faster_whisper import WhisperModel

# Global model instance loaded once at module level (lazy loaded on first reference to avoid blocking import)
_whisper_model = None


def _get_model() -> WhisperModel:
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
    return _whisper_model


def extract_text_from_audio(file_path: str) -> list[dict]:
    """
    Transcribes audio using faster-whisper and extracts segments with timestamp ranges.
    Returns a list of dicts: {"text": "<segment text>", "source": "<filename>", "page": "<start_time>-<end_time>", "type": "audio"}
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    filename = os.path.basename(file_path)
    model = _get_model()

    segments, _ = model.transcribe(file_path, beam_size=5)

    results = []
    for segment in segments:
        text = segment.text.strip()
        if text:
            time_range = f"{segment.start:.1f}s-{segment.end:.1f}s"
            results.append({
                "text": text,
                "source": filename,
                "page": time_range,
                "type": "audio"
            })

    return results
