"""
Main launcher and PyInstaller entrypoint for the Offline Multimodal RAG Assistant.
"""
import os
import sys
import webbrowser
import threading
import time
import streamlit.web.cli as stcli

# Ensure console output uses safe encoding on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure root package is in sys.path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

try:
    from launcher.first_run_setup import ensure_ready
except ImportError:
    from first_run_setup import ensure_ready


def get_app_path() -> str:
    """
    Resolves the absolute path to app.py whether running as source or frozen binary.
    """
    if getattr(sys, "frozen", False):
        # PyInstaller extracts bundled files to sys._MEIPASS or alongside executable
        base_dir = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        app_path = os.path.join(base_dir, "app.py")
        if os.path.exists(app_path):
            return app_path
        # Fallback to alongside executable directory
        exe_dir = os.path.dirname(sys.executable)
        app_path = os.path.join(exe_dir, "app.py")
        if os.path.exists(app_path):
            return app_path
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, "app.py")

    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app.py")


def main():
    print("========================================================")
    print("       Starting Offline Multimodal RAG Assistant...     ")
    print("========================================================")
    print()

    def console_progress(msg: str):
        try:
            print(f"[SETUP] {msg}")
        except Exception:
            pass

    try:
        ensure_ready(progress_callback=console_progress)
    except Exception as e:
        print("\n" + "=" * 56)
        print(" [ERROR] Setup encountered an issue:")
        print(f" {str(e)}")
        print("=" * 56)
        try:
            input("\nPress Enter to exit...")
        except Exception:
            pass
        sys.exit(1)

    app_path = get_app_path()
    if not os.path.exists(app_path):
        print(f"[ERROR] Could not locate application file: {app_path}")
        input("\nPress Enter to exit...")
        sys.exit(1)

    print("\n[READY] Launching web interface on http://localhost:8501 ...")

    # Launch browser automatically in background thread
    def open_browser():
        time.sleep(2.0)
        try:
            webbrowser.open("http://localhost:8501")
        except Exception:
            pass

    threading.Thread(target=open_browser, daemon=True).start()

    # Programmatic Streamlit launch
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--global.developmentMode=false",
        "--server.headless=false",
        "--browser.serverAddress=localhost",
        "--server.port=8501",
    ]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
