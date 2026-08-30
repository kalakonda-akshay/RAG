"""
Manages persistent chat session saving, loading, listing, and deletion.
"""
import os
import json

_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
SESSIONS_DIR = os.path.join(_parent_dir, "data", "sessions")
os.makedirs(SESSIONS_DIR, exist_ok=True)


def list_sessions() -> list[str]:
    """
    Returns a list of saved session names.
    """
    if not os.path.exists(SESSIONS_DIR):
        return []
    files = [f[:-5] for f in os.listdir(SESSIONS_DIR) if f.endswith(".json")]
    return sorted(files, reverse=True)


def save_session(session_name: str, messages: list[dict]) -> str:
    """
    Saves a chat history session to JSON file.
    """
    safe_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in session_name)
    filepath = os.path.join(SESSIONS_DIR, f"{safe_name}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2)
    return filepath


def load_session(session_name: str) -> list[dict]:
    """
    Loads a saved chat history session.
    """
    safe_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in session_name)
    filepath = os.path.join(SESSIONS_DIR, f"{safe_name}.json")
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def delete_session(session_name: str) -> bool:
    """
    Deletes a saved session file.
    """
    safe_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in session_name)
    filepath = os.path.join(SESSIONS_DIR, f"{safe_name}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False
