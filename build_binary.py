"""
Build script to compile OfflineRAGAssistant executable using PyInstaller.
"""
import os
import sys
import subprocess
import shutil
import streamlit

# Root directories
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STREAMLIT_DIR = os.path.dirname(streamlit.__file__)

print(f"Building OfflineRAGAssistant from {PROJECT_DIR}...")
print(f"Streamlit library directory: {STREAMLIT_DIR}")

# Build PyInstaller command
cmd = [
    sys.executable,
    "-m",
    "PyInstaller",
    "--noconfirm",
    "--onedir",
    "--console",
    "--name", "OfflineRAGAssistant",
    # Add project files
    "--add-data", f"{os.path.join(PROJECT_DIR, 'app.py')};.",
    "--add-data", f"{os.path.join(PROJECT_DIR, 'ingestion')};ingestion",
    "--add-data", f"{os.path.join(PROJECT_DIR, 'core')};core",
    "--add-data", f"{os.path.join(PROJECT_DIR, 'launcher')};launcher",
    "--add-data", f"{os.path.join(PROJECT_DIR, 'data')};data",
    "--add-data", f"{STREAMLIT_DIR};streamlit",
    # Collect metadata and submodules
    "--collect-all", "streamlit",
    "--collect-all", "chromadb",
    "--collect-all", "faster_whisper",
    "--collect-all", "pymupdf",
    "--collect-all", "docx",
    "--collect-all", "langchain_text_splitters",
    "--collect-all", "ollama",
    "--collect-all", "pytesseract",
    "--collect-all", "PIL",
    # Entry point
    os.path.join(PROJECT_DIR, "launcher", "run_app.py")
]

print("Executing PyInstaller command...")
result = subprocess.run(cmd, cwd=PROJECT_DIR)
if result.returncode == 0:
    print("\n✓ PyInstaller build succeeded!")
    print(f"Output directory: {os.path.join(PROJECT_DIR, 'dist', 'OfflineRAGAssistant')}")
else:
    print(f"\n❌ PyInstaller build failed with exit code {result.returncode}")
    sys.exit(result.returncode)
