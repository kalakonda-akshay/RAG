"""
Streamlit entrypoint for the Offline Multimodal RAG Assistant (Upgraded Edition).
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
    page_icon="🧠",
    layout="wide",
)


# 2. Startup Check — Ollama Health & Model List
def get_installed_models() -> list[str]:
    try:
        models_data = ollama.list()
        model_names = []
        for m in models_data.get("models", []):
            if isinstance(m, dict):
                name = m.get("name", "")
            else:
                name = getattr(m, "model", str(m))
            if name:
                model_names.append(name)
        return model_names if model_names else ["llama3.2:3b"]
    except Exception:
        return []

installed_models = get_installed_models()
if not installed_models:
    st.error("⚠️ Ollama is not running. Start it with: `ollama serve`")
    st.info("Make sure the local Ollama server is active and required models are pulled (`llama3.2:3b`, `nomic-embed-text`).")
    st.stop()


# 3. Custom Theme & Styling Injection
st.markdown("""
<style>
/* Main container max-width & spacing */
.main .block-container {
    max-width: 960px;
    padding-top: 1.75rem;
    padding-bottom: 4rem;
}

/* Gradient Heading */
.gradient-header {
    background: linear-gradient(135deg, #6366F1 0%, #A855F7 60%, #EC4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.25rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    margin-bottom: 0.25rem;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}

/* Subtitle */
.sub-header-text {
    color: #9CA3AF;
    font-size: 1.05rem;
    line-height: 1.5;
    margin-bottom: 1.25rem;
}

/* Accent Line */
.header-accent-line {
    height: 2px;
    background: linear-gradient(90deg, #6366F1 0%, #A855F7 50%, transparent 100%);
    border-radius: 9999px;
    margin-bottom: 1.5rem;
}

/* Button Styling & Hover Lift */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(99, 102, 241, 0.25) !important;
}

/* Rounded UI Components */
[data-testid="stFileUploader"] {
    border-radius: 12px !important;
}

[data-testid="stChatInput"] {
    border-radius: 12px !important;
}

/* Chat Message Bubble Styling */
[data-testid="stChatMessage"] {
    border-radius: 14px !important;
    padding: 1rem 1.25rem !important;
    margin-bottom: 1.25rem !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    background-color: #161922 !important;
}

/* Source Badges */
.source-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background-color: #202434;
    border: 1px solid #374151;
    border-radius: 9999px;
    padding: 0.3rem 0.75rem;
    margin: 0.2rem 0.3rem 0.2rem 0;
    font-size: 0.82rem;
    color: #E5E7EB;
}

.source-chip-marker {
    color: #818CF8;
    font-weight: 700;
    font-size: 0.85rem;
}

/* Indexed file badges in sidebar */
.indexed-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: #C7D2FE;
    padding: 0.25rem 0.6rem;
    border-radius: 8px;
    font-size: 0.82rem;
    margin-bottom: 0.4rem;
    margin-right: 0.3rem;
    word-break: break-all;
}

/* Empty State Card */
.empty-state-card {
    text-align: center;
    padding: 3.5rem 1.5rem;
    border: 1px dashed rgba(255, 255, 255, 0.15);
    border-radius: 16px;
    background: rgba(26, 29, 41, 0.4);
    margin: 2rem 0;
}

.empty-state-icon {
    font-size: 3rem;
    margin-bottom: 0.75rem;
}

.empty-state-title {
    font-size: 1.35rem;
    font-weight: 600;
    color: #F3F4F6;
    margin-bottom: 0.5rem;
}

.empty-state-desc {
    color: #9CA3AF;
    font-size: 0.95rem;
    max-width: 460px;
    margin: 0 auto;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

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
if "current_workspace" not in st.session_state:
    st.session_state.current_workspace = "documents"


def render_sources(sources: list[dict]):
    """
    Renders sources sorted ascending by their numeric [n] marker inside styled badge chips.
    """
    if not sources:
        return

    def parse_marker(item: dict) -> int:
        marker_str = item.get("marker", "").strip("[]")
        return int(marker_str) if marker_str.isdigit() else 999

    sorted_sources = sorted(sources, key=parse_marker)
    with st.expander("📚 Sources", expanded=False):
        chips_html = '<div style="display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.25rem;">'
        for src in sorted_sources:
            marker = src.get("marker", "")
            filename = src.get("source", "")
            page = src.get("page", "")
            page_str = f"page {page}" if str(page).isdigit() else str(page)
            chips_html += f'<span class="source-chip"><span class="source-chip-marker">{marker}</span> <b>{filename}</b> &middot; {page_str}</span>'
        chips_html += '</div>'
        st.markdown(chips_html, unsafe_allow_html=True)


# 4. Sidebar — Ingestion & Controls
with st.sidebar:
    st.title("📂 Settings & Ingestion")

    # Model Selector
    st.subheader("🤖 Local Model")
    selected_model = st.selectbox(
        "Choose LLM model:",
        options=installed_models,
        index=0 if "llama3.2:3b" not in installed_models else installed_models.index("llama3.2:3b"),
        help="Select any local model running in your Ollama library.",
    )

    # Workspace Collection Selector
    st.subheader("🗂️ Workspace Collection")
    workspace_choice = st.selectbox(
        "Active collection:",
        options=["documents", "finance", "research", "engineering"],
        index=0,
        help="Separate your files into distinct project collections.",
    )
    st.session_state.current_workspace = workspace_choice

    st.divider()

    st.subheader("📥 Upload Multimodal Files")
    uploaded_files = st.file_uploader(
        "Upload files",
        type=[
            "pdf", "docx", "pptx", "ppt", "png", "jpg", "jpeg", "wav", "mp3", "m4a",
            "csv", "xlsx", "xls", "mp4", "mkv", "mov", "avi", "txt", "md", "py", "js", "json", "html"
        ],
        accept_multiple_files=True,
        help="Supported: PDFs, Word, PowerPoint, Excel/CSV, Videos, Audio, Images (OCR), Text/Code",
    )

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
                            st.warning(f"No text could be extracted from {file.name}.")
                            continue

                        chunks = chunk_documents(raw_docs)
                        if not chunks:
                            st.warning(f"No text could be extracted from {file.name}.")
                            continue

                        add_chunks(chunks, collection_name=st.session_state.current_workspace)

                        if file.name not in st.session_state.indexed_files:
                            st.session_state.indexed_files.append(file.name)

                        st.success(f"✓ Processed {file.name} ({len(chunks)} chunks)")
                except Exception as e:
                    st.error(f"Failed to process {file.name}: {str(e)}")

                progress_bar.progress((idx + 1) / total_files, text=f"Processed {idx + 1}/{total_files} files")

    st.divider()

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
        help="Loads sample documents from data/demo/",
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
                        st.warning(f"No text could be extracted from {demo_name}.")
                        continue

                    chunks = chunk_documents(raw_docs)
                    if not chunks:
                        st.warning(f"No text could be extracted from {demo_name}.")
                        continue

                    add_chunks(chunks, collection_name=st.session_state.current_workspace)

                    if demo_name not in st.session_state.indexed_files:
                        st.session_state.indexed_files.append(demo_name)

                    st.success(f"✓ Loaded demo {demo_name} ({len(chunks)} chunks)")
            except Exception as e:
                st.error(f"Failed to load demo file {demo_name}: {str(e)}")

            demo_progress.progress((d_idx + 1) / demo_total, text=f"Processed {d_idx + 1}/{demo_total} demo files")

    st.divider()

    # Indexed Files List
    st.subheader("📚 Indexed Documents")
    if st.session_state.indexed_files:
        st.write(f"**Indexed documents ({len(st.session_state.indexed_files)}):**")
        pills_html = '<div style="display: flex; flex-wrap: wrap; gap: 0.3rem;">'
        for filename in st.session_state.indexed_files:
            pills_html += f'<div class="indexed-pill">📄 <span>{filename}</span></div>'
        pills_html += '</div>'
        st.markdown(pills_html, unsafe_allow_html=True)
    else:
        st.info("No files indexed yet. Upload documents above to start querying.")

    st.divider()

    # Chat History Export
    st.subheader("💾 Export Report")
    if st.session_state.messages:
        report_md = "# Offline RAG Chat Report\n\n"
        for m in st.session_state.messages:
            role = "User" if m["role"] == "user" else "Assistant"
            report_md += f"### {role}\n{m['content']}\n\n"
        st.download_button(
            "Download Chat Report (.md)",
            data=report_md,
            file_name="OfflineRAG_Chat_Report.md",
            mime="text/markdown",
            use_container_width=True,
        )
    else:
        st.caption("Chat history empty — start typing to generate a report.")

    st.divider()

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
                client.delete_collection(st.session_state.current_workspace)
            except Exception:
                pass
            st.session_state.messages = []
            st.session_state.indexed_files = []
            st.success("Vector store and chat history reset successfully.")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to reset vector index: {str(e)}")


# 5. Main Area — Header & How It Works Container
col_l, col_center, col_r = st.columns([0.02, 0.96, 0.02])
with col_center:
    st.markdown(f"""
    <div class="gradient-header">
        <span>🧠</span> Offline Multimodal RAG Assistant
    </div>
    <div class="sub-header-text">
        Ask questions across PDFs (native & scanned), Excel/CSV, PowerPoints, Videos, Audio, Images, and Code — 100% offline.
    </div>
    <div class="header-accent-line"></div>
    """, unsafe_allow_html=True)

    with st.expander("ℹ️ How it works", expanded=False):
        st.markdown(f"""
        - **Local Multimodal Ingestion**: Supports PDFs (native & scanned OCR), Word, PowerPoint, Excel/CSV, Videos (audio extraction), Audio (Whisper), Images (Tesseract OCR), and Code/Text.
        - **Hybrid Search Engine**: Combines BM25 Keyword Matching + Dense Vector Cosine Similarity (Reciprocal Rank Fusion) on ChromaDB.
        - **Multi-Turn Chat Memory**: Remembers recent conversation history for natural follow-up questions.
        - **Active Model & Workspace**: Running `{selected_model}` in workspace `{st.session_state.current_workspace}`.
        """)

# 6. Empty State (when no chat history and no files)
if not st.session_state.messages and not st.session_state.indexed_files:
    st.markdown("""
    <div class="empty-state-card">
        <div class="empty-state-icon">📂</div>
        <div class="empty-state-title">Upload a file to get started</div>
        <div class="empty-state-desc">
            Drag & drop PDFs, Excel sheets, PowerPoints, Video/Audio files, or Code in the sidebar to build your private local knowledge base.
        </div>
    </div>
    """, unsafe_allow_html=True)

# 7. Render Chat Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            render_sources(msg["sources"])

# 8. Chat Input Handling
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
                    result = generate_answer(
                        clean_prompt,
                        model=selected_model,
                        collection_name=st.session_state.current_workspace,
                        chat_history=st.session_state.messages,
                    )
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
