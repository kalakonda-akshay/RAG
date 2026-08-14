"""
First-run setup and dependency verification for Ollama and required models.
"""
import os
import sys
import shutil
import subprocess
import time
import requests

# Ensure console output uses safe encoding
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def get_ollama_executable() -> str | None:
    """
    Finds the Ollama executable path on PATH or standard install locations.
    """
    which_path = shutil.which("ollama")
    if which_path:
        return which_path

    if os.name == "nt":
        common_paths = [
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama.exe"),
            r"C:\Program Files\Ollama\ollama.exe",
            r"C:\Program Files (x86)\Ollama\ollama.exe",
        ]
        for path in common_paths:
            if os.path.exists(path):
                return path

    return None


def is_ollama_installed() -> bool:
    """
    Checks if Ollama is installed and available on PATH or in standard directories.
    """
    return get_ollama_executable() is not None


def is_ollama_running() -> bool:
    """
    Checks if the local Ollama API server is running and responding on http://localhost:11434.
    """
    try:
        response = requests.get("http://localhost:11434/api/version", timeout=2)
        return response.status_code == 200
    except Exception:
        return False


def start_ollama() -> None:
    """
    Launches 'ollama serve' as a background subprocess and waits up to 10 seconds for it to become ready.
    """
    ollama_cmd = get_ollama_executable() or "ollama"
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0

    try:
        subprocess.Popen(
            [ollama_cmd, "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=flags,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to launch Ollama service: {e}") from e

    # Poll up to 10 seconds for server readiness
    for _ in range(20):
        time.sleep(0.5)
        if is_ollama_running():
            return

    if not is_ollama_running():
        raise RuntimeError("Ollama server was started but did not respond within 10 seconds.")


def is_model_pulled(model_name: str) -> bool:
    """
    Runs 'ollama list' and checks if model_name is present in the downloaded models list.
    """
    ollama_cmd = get_ollama_executable() or "ollama"
    try:
        result = subprocess.run(
            [ollama_cmd, "list"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        return model_name in result.stdout
    except Exception:
        return False


def pull_model(model_name: str, progress_callback=None) -> None:
    """
    Runs 'ollama pull <model_name>' streaming output line-by-line and invoking progress_callback.
    Uses UTF-8 encoding with character replacement to prevent Windows cp1252 decoding crashes.
    """
    ollama_cmd = get_ollama_executable() or "ollama"
    process = subprocess.Popen(
        [ollama_cmd, "pull", model_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
        universal_newlines=True,
    )

    if process.stdout:
        for line in process.stdout:
            clean_line = line.strip()
            if clean_line and progress_callback:
                progress_callback(clean_line)

    process.wait()
    if process.returncode != 0:
        raise RuntimeError(f"Failed to pull model '{model_name}'. Exit code: {process.returncode}")


def ensure_ready(progress_callback=None) -> None:
    """
    Orchestrates full readiness check:
    1. Verifies Ollama is installed (raises clear error if missing)
    2. Starts Ollama if not running
    3. Ensures 'llama3.2:3b' and 'nomic-embed-text' are pulled
    """
    if progress_callback:
        progress_callback("Checking Ollama installation...")

    if not is_ollama_installed():
        raise RuntimeError(
            "Ollama is not installed or not found on PATH.\n"
            "Please install Ollama from https://ollama.com or run the installer again."
        )

    if not is_ollama_running():
        if progress_callback:
            progress_callback("Starting local Ollama server...")
        start_ollama()

    required_models = ["llama3.2:3b", "nomic-embed-text"]
    for model in required_models:
        if not is_model_pulled(model):
            if progress_callback:
                progress_callback(f"Downloading required model: {model} (this may take a few minutes on first run)...")
            pull_model(model, progress_callback=progress_callback)
        else:
            if progress_callback:
                progress_callback(f"Model ready: {model}")

    if progress_callback:
        progress_callback("All local AI services and models are ready!")
