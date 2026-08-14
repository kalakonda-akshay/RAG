"""
Streamlit entrypoint for the Offline Multimodal RAG Assistant.
"""
import os
import streamlit as st
import ollama

from ingestion.router import process_file
from core.chunker import chunk_documents
from core.vectorstore import add_chunks, _get_client
from core.rag_engine import generate_answer

# 1. Page Configuration
st.set_page_config(
    page_title="Offline Multimodal RAG Assistant",
    page_icon="🔍",
    layout="wide",
)

# 2. Startup Check — Ollama Health
def is_ollama_running() -> bool:
    try:
        ollama.list()
        return True
    except Exception:
        return False

if not is_ollama_running():
    st.error("⚠️ Ollama is not running. Start it with: `ollama serve`")
    st.info("Make sure the local Ollama server is active and the required models are pulled (`llama3.2:3b`, `nomic-embed-text`).")
    st.stop()

# Workspace Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "data", "uploads")
DEMO_DIR = os.path.join(BASE_DIR, "data", "demo")
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(DEMO_DIR, exist_ok=True)

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = []


def render_sources(sources: list[dict]):
    """
    Renders sources sorted ascending by their numeric [n] marker.
    """
    if not sources:
        return

    def parse_marker(item: dict) -> int:
        marker_str = item.get("marker", "").strip("[]")
        return int(marker_str) if marker_str.isdigit() else 999

    sorted_sources = sorted(sources, key=parse_marker)
    with st.expander("Sources"):
        for src in sorted_sources:
            marker = src.get("marker", "")
            filename = src.get("source", "")
            page = src.get("page", "")
            page_str = f"page {page}" if str(page).isdigit() else str(page)
            st.markdown(f"**{marker}** `{filename}` — {page_str}")


# 3. Sidebar — Ingestion & Controls
with st.sidebar:
    st.title("📂 Document Ingestion")
    st.write("Upload local multimodal documents into the offline vector store.")

    uploaded_files = st.file_uploader(
        "Upload files",
        type=["pdf", "docx", "png", "jpg", "jpeg", "wav", "mp3", "m4a"],
        accept_multiple_files=True,
        help="Supported formats: PDF, DOCX, Images (OCR), Audio (Whisper)",
    )

    # Show file details before processing
    if uploaded_files:
        st.markdown("**Selected files:**")
        for f in uploaded_files:
            ext = os.path.splitext(f.name)[1].lower().lstrip(".")
            size_kb = f.size / 1024
            st.caption(f"📄 `{f.name}` ({ext.upper()}, {size_kb:.1f} KB)")

    if st.button("Process Files", type="primary", use_container_width=True):
        if not uploaded_files:
            st.warning("Please choose at least one file to upload.")
        else:
            total_files = len(uploaded_files)
            progress_bar = st.progress(0, text="Starting ingestion...")
            for idx, file in enumerate(uploaded_files):
                file_path = os.path.join(UPLOADS_DIR, file.name)
                try:
                    with st.spinner(f"Processing {file.name}..."):
                        with open(file_path, "wb") as f_out:
                            f_out.write(file.getbuffer())

                        raw_docs = process_file(file_path)
                        if not raw_docs:
                            st.warning(f"No text could be extracted from {file.name} — it may be a scanned/empty file.")
                            continue

                        chunks = chunk_documents(raw_docs)
                        if not chunks:
                            st.warning(f"No text could be extracted from {file.name} — it may be a scanned/empty file.")
                            continue

                        add_chunks(chunks)

                        if file.name not in st.session_state.indexed_files:
                            st.session_state.indexed_files.append(file.name)

                        st.success(f"✓ Processed {file.name} ({len(chunks)} chunks)")
                except Exception as e:
                    st.error(f"Failed to process {file.name}: {str(e)}")

                progress_bar.progress((idx + 1) / total_files, text=f"Processed {idx + 1}/{total_files} files")

    st.markdown("---")

    # Demo Data Integration
    st.subheader("🎯 Demo Data")
    demo_files = [
        f for f in os.listdir(DEMO_DIR)
        if os.path.isfile(os.path.join(DEMO_DIR, f)) and not f.startswith(".")
    ]
    has_demo_files = len(demo_files) > 0

    if st.button(
        "Load Demo Data",
        disabled=not has_demo_files,
        help="Loads sample documents from data/demo/" if has_demo_files else "No demo files found in data/demo/",
        use_container_width=True,
    ):
        demo_total = len(demo_files)
        demo_progress = st.progress(0, text="Loading demo documents...")
        for d_idx, demo_name in enumerate(demo_files):
            demo_path = os.path.join(DEMO_DIR, demo_name)
            try:
                with st.spinner(f"Processing demo file: {demo_name}..."):
                    raw_docs = process_file(demo_path)
                    if not raw_docs:
                        st.warning(f"No text could be extracted from {demo_name} — it may be a scanned/empty file.")
                        continue

                    chunks = chunk_documents(raw_docs)
                    if not chunks:
                        st.warning(f"No text could be extracted from {demo_name} — it may be a scanned/empty file.")
                        continue

                    add_chunks(chunks)

                    if demo_name not in st.session_state.indexed_files:
                        st.session_state.indexed_files.append(demo_name)

                    st.success(f"✓ Loaded demo {demo_name} ({len(chunks)} chunks)")
            except Exception as e:
                st.error(f"Failed to load demo file {demo_name}: {str(e)}")

            demo_progress.progress((d_idx + 1) / demo_total, text=f"Processed {d_idx + 1}/{demo_total} demo files")

    st.markdown("---")

    # Indexed Files List
    st.subheader("📚 Indexed Documents")
    if st.session_state.indexed_files:
        st.write(f"**Indexed files ({len(st.session_state.indexed_files)}):**")
        for filename in st.session_state.indexed_files:
            st.markdown(f"- `{filename}`")
    else:
        st.info("No files indexed yet. Upload documents above to start querying.")

    st.markdown("---")

    # Clear Index & Reset
    st.subheader("⚙️ Reset Index")
    confirm_reset = st.checkbox(
        "Confirm database reset",
        help="Check this box to enable clearing the ChromaDB vector store and chat history.",
    )
    if st.button("Clear Index", type="secondary", disabled=not confirm_reset, use_container_width=True):
        try:
            client = _get_client()
            try:
                client.delete_collection("documents")
            except Exception:
                pass
            st.session_state.messages = []
            st.session_state.indexed_files = []
            st.success("Vector store and chat history reset successfully.")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to reset vector index: {str(e)}")


# 4. Main Area — Header & How It Works
st.title("Offline Multimodal RAG Assistant")
st.caption("Ask questions across your PDFs, Word docs, images, and audio — fully offline, with cited sources.")

with st.expander("ℹ️ How it works", expanded=False):
    st.markdown("""
    - **Local Multimodal Ingestion**: Files are processed entirely on your machine without cloud services (PDFs via PyMuPDF, Word via python-docx, Images via Tesseract OCR, and Audio via faster-whisper).
    - **Semantic Chunking & Embedding**: Content is split into chunks and embedded locally using Ollama (`nomic-embed-text`).
    - **Offline Vector Search**: High-dimensional vector search runs locally on ChromaDB.
    - **Grounded Answer Generation**: Local LLM (`llama3.2:3b`) synthesizes answers with source citations (`[1]`, `[2]`) referencing the exact page or audio timestamp.
    """)

# 5. Render Chat Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            render_sources(msg["sources"])

# 6. Chat Input Handling
if prompt := st.chat_input("Ask a question about your documents..."):
    clean_prompt = prompt.strip()
    if not clean_prompt:
        st.stop()

    if not st.session_state.indexed_files:
        st.warning("Please upload and process at least one file first.")
    else:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": clean_prompt})
        with st.chat_message("user"):
            st.markdown(clean_prompt)

        # Generate Assistant Response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = generate_answer(clean_prompt)
                    answer_text = result.get("answer", "No response generated.")
                    sources = result.get("sources", [])

                    st.markdown(answer_text)
                    if sources:
                        render_sources(sources)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer_text,
                        "sources": sources,
                    })
                except Exception as e:
                    error_message = f"Error: {str(e)}"
                    st.error(error_message)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_message,
                        "sources": [],
                    })

st.caption("Answers are generated only from your uploaded files.")
