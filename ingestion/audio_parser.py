"""
Handles audio transcription using faster-whisper with intelligent segment grouping.
"""
import os
from faster_whisper import WhisperModel

# Global model instance loaded once at module level (lazy loaded on first reference)
_whisper_model = None


def _get_model() -> WhisperModel:
    global _whisper_model
    if _whisper_model is None:
        # Load 'base' model on CPU with int8 quantization for high accuracy & fast offline execution
        _whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
    return _whisper_model


def _format_time(seconds: float) -> str:
    """
    Formats seconds into MM:SS format.
    """
    mins, secs = divmod(int(seconds), 60)
    return f"{mins:02d}:{secs:02d}"


def extract_text_from_audio(file_path: str) -> list[dict]:
    """
    Transcribes audio using faster-whisper and groups short segments into cohesive,
    semantically meaningful chunks (~40-80 words or natural pauses) for superior RAG indexing.
    Returns a list of dicts:
    {"text": "<transcription text>", "source": "<filename>", "page": "<start_time> - <end_time>", "type": "audio"}
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    filename = os.path.basename(file_path)
    model = _get_model()

    try:
        segments_gen, info = model.transcribe(
            file_path,
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500),
        )
        segments = list(segments_gen)
    except Exception:
        # Fallback without vad_filter if audio format is unusual
        segments_gen, info = model.transcribe(file_path, beam_size=5)
        segments = list(segments_gen)

    if not segments:
        return []

    results = []
    current_texts = []
    current_start = None
    current_end = None
    current_word_count = 0

    for seg in segments:
        text = seg.text.strip()
        if not text:
            continue

        if current_start is None:
            current_start = seg.start
        current_end = seg.end

        current_texts.append(text)
        current_word_count += len(text.split())

        # Group into cohesive chunks of ~50-80 words or 30+ seconds for optimal RAG context
        if current_word_count >= 50 or (current_end - current_start >= 30.0):
            combined_text = " ".join(current_texts).strip()
            time_range = f"{_format_time(current_start)} - {_format_time(current_end)}"
            results.append({
                "text": combined_text,
                "source": filename,
                "page": time_range,
                "type": "audio",
            })
            current_texts = []
            current_start = None
            current_end = None
            current_word_count = 0

    # Append remaining trailing segment
    if current_texts and current_start is not None and current_end is not None:
        combined_text = " ".join(current_texts).strip()
        time_range = f"{_format_time(current_start)} - {_format_time(current_end)}"
        results.append({
            "text": combined_text,
            "source": filename,
            "page": time_range,
            "type": "audio",
        })

    return results
