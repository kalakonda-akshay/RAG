"""
Detects file type and routes to the appropriate parser for multimodal document processing.
"""
import os
import sys

_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

try:
    from ingestion.pdf_parser import extract_text_from_pdf
    from ingestion.docx_parser import extract_text_from_docx
    from ingestion.pptx_parser import extract_text_from_pptx
    from ingestion.image_parser import extract_text_from_image
    from ingestion.audio_parser import extract_text_from_audio
    from ingestion.excel_parser import extract_text_from_excel
    from ingestion.video_parser import extract_text_from_video
    from ingestion.text_parser import extract_text_from_textfile
except ImportError:
    from pdf_parser import extract_text_from_pdf
    from docx_parser import extract_text_from_docx
    from pptx_parser import extract_text_from_pptx
    from image_parser import extract_text_from_image
    from audio_parser import extract_text_from_audio
    from excel_parser import extract_text_from_excel
    from video_parser import extract_text_from_video
    from text_parser import extract_text_from_textfile


EXT_MAP = {
    ".pdf": extract_text_from_pdf,
    ".docx": extract_text_from_docx,
    ".pptx": extract_text_from_pptx,
    ".ppt": extract_text_from_pptx,
    ".png": extract_text_from_image,
    ".jpg": extract_text_from_image,
    ".jpeg": extract_text_from_image,
    ".wav": extract_text_from_audio,
    ".mp3": extract_text_from_audio,
    ".m4a": extract_text_from_audio,
    ".csv": extract_text_from_excel,
    ".xlsx": extract_text_from_excel,
    ".xls": extract_text_from_excel,
    ".mp4": extract_text_from_video,
    ".mkv": extract_text_from_video,
    ".mov": extract_text_from_video,
    ".avi": extract_text_from_video,
    ".txt": extract_text_from_textfile,
    ".md": extract_text_from_textfile,
    ".py": extract_text_from_textfile,
    ".js": extract_text_from_textfile,
    ".json": extract_text_from_textfile,
    ".html": extract_text_from_textfile,
    ".xml": extract_text_from_textfile,
    ".sql": extract_text_from_textfile,
}


def process_file(file_path: str) -> list[dict]:
    """
    Detects file type by extension and calls the corresponding parser.
    Raises ValueError for unsupported file types.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    _, ext = os.path.splitext(file_path)
    ext_lower = ext.lower()

    parser = EXT_MAP.get(ext_lower)
    if parser is None:
        supported = ", ".join(sorted(EXT_MAP.keys()))
        raise ValueError(
            f"Unsupported file type '{ext}'. Supported file types are: {supported}"
        )

    return parser(file_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ingestion/router.py <path/to/file>")
        sys.exit(1)

    target_path = sys.argv[1]
    result = process_file(target_path)
    print(result)
