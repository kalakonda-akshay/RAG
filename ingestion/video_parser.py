"""
Handles video file (.mp4, .mkv, .mov, .avi) audio extraction and Whisper transcription.
"""
import os
import sys
import tempfile
import subprocess

_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

try:
    import imageio_ffmpeg
except ImportError:
    imageio_ffmpeg = None

try:
    from ingestion.audio_parser import extract_text_from_audio
except ImportError:
    from audio_parser import extract_text_from_audio


def extract_text_from_video(file_path: str) -> list[dict]:
    """
    Extracts the audio stream from a video file using ffmpeg and transcribes it using Whisper.
    Returns a list of dicts: {"text": "<transcript>", "source": "<filename>", "page": "<timestamp>", "type": "video"}
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if imageio_ffmpeg is None:
        raise RuntimeError("imageio_ffmpeg library is not available. Please install imageio-ffmpeg.")

    filename = os.path.basename(file_path)
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    # Create temporary WAV file for extracted audio
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio:
        tmp_audio_path = tmp_audio.name

    try:
        # Extract audio stream at 16kHz mono WAV for Whisper
        cmd = [
            ffmpeg_exe,
            "-y",
            "-i", file_path,
            "-vn",  # Disable video
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            tmp_audio_path,
        ]
        flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=flags)
        if res.returncode != 0:
            raise RuntimeError(f"Failed to extract audio from video '{filename}': {res.stderr.decode('utf-8', errors='ignore')}")

        # Run Whisper transcription on extracted audio
        transcripts = extract_text_from_audio(tmp_audio_path)

        # Override source filename and type to video
        results = []
        for item in transcripts:
            item["source"] = filename
            item["type"] = "video"
            results.append(item)

        return results
    finally:
        if os.path.exists(tmp_audio_path):
            try:
                os.remove(tmp_audio_path)
            except Exception:
                pass
