"""
Real-Time Voice-to-Voice Conversational RAG Loop (Whisper STT -> RAG Engine -> pyttsx3 TTS).
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
    from ingestion.audio_parser import extract_text_from_audio
    from core.rag_engine import generate_answer
    from core.tts_engine import speak_text_to_file
except ImportError:
    from audio_parser import extract_text_from_audio
    from rag_engine import generate_answer
    from tts_engine import speak_text_to_file


def process_voice_turn(
    audio_bytes: bytes,
    model: str = "llama3.2:3b",
    workspace: str = "documents",
    persona: str = "General Assistant",
    chat_history: list[dict] = None,
) -> dict:
    """
    Processes a complete voice interaction turn:
    Voice Input -> Whisper STT -> RAG LLM -> Text-to-Speech Output Audio.
    """
    if not audio_bytes:
        return {"transcript": "", "answer": "No audio detected.", "sources": [], "audio_path": None}

    # Save audio input bytes
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_in:
        tmp_in_path = tmp_in.name
        tmp_in.write(audio_bytes)

    try:
        # 1. Transcribe voice input with Whisper
        transcripts = extract_text_from_audio(tmp_in_path)
        spoken_text = " ".join([t.get("text", "") for t in transcripts]).strip()

        if not spoken_text:
            return {"transcript": "", "answer": "Could not understand audio speech.", "sources": [], "audio_path": None}

        # 2. Query RAG engine
        result = generate_answer(
            question=spoken_text,
            model=model,
            collection_name=workspace,
            persona_name=persona,
            chat_history=chat_history,
        )
        answer_text = result.get("answer", "")
        sources = result.get("sources", [])

        # 3. Synthesize response speech audio
        audio_out_path = speak_text_to_file(answer_text)

        return {
            "transcript": spoken_text,
            "answer": answer_text,
            "sources": sources,
            "audio_path": audio_out_path,
        }
    finally:
        if os.path.exists(tmp_in_path):
            try:
                os.remove(tmp_in_path)
            except Exception:
                pass
