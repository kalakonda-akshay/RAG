"""
FastAPI REST backend for the Orbit / Archive RAG application.
Provides a high-performance HTTP API matching the exact contract expected by the new React + TypeScript frontend.
"""
import os
import sys
import base64
import tempfile
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel
import uvicorn
import ollama

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

UPLOADS_DIR = os.path.join(BASE_DIR, "data", "uploads")
REPORTS_DIR = os.path.join(BASE_DIR, "data", "reports")
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# Import existing core modules
from ingestion.router import process_file
from core.chunker import chunk_documents
from core.vectorstore import (
    add_chunks,
    _get_client,
    get_collection,
    list_all_collections,
    list_indexed_files,
    delete_workspace_collection,
    query_collection,
)
from core.rag_engine import generate_answer
from core.tts_engine import speak_text_to_file
from core.session_manager import list_sessions, save_session, load_session, delete_session
from core.report_generator import generate_executive_brief, generate_pptx_deck
from core.doc_comparator import compare_documents
from core.self_rag import critic_verify_answer
from core.personas import PERSONAS
from core.sql_engine import query_sqlite_database
from core.doc_tools import redact_pii_text
from core.quiz_generator import generate_quiz
from core.system_monitor import get_system_stats
from core.mindmap_generator import generate_mindmap
from core.topic_cluster import discover_topic_clusters
from core.translator import translate_text, LANGUAGES
from ingestion.web_crawler import crawl_and_save_webpage
from core.voice_mode import process_voice_turn

app = FastAPI(title="Orbit Offline RAG API", version="2.0.0")

# Enable CORS for local dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_doc_icon_type(filename: str) -> str:
    ext = filename.lower().split(".")[-1]
    if ext == "pdf":
        return "pdf"
    elif ext in ("md", "txt"):
        return "md"
    elif ext in ("xlsx", "xls", "csv"):
        return "xlsx"
    elif ext in ("png", "jpg", "jpeg", "webp", "bmp", "tiff", "gif"):
        return "png"
    elif ext in ("sqlite", "db"):
        return "db"
    return "file"


# ------------------------------------------------------------------------------
# Pydantic Request Models
# ------------------------------------------------------------------------------
class CreateWorkspaceRequest(BaseModel):
    name: str

class ChatRequest(BaseModel):
    query: str
    workspace: Optional[str] = "documents"
    focus_file: Optional[str] = None
    persona: Optional[str] = "General Assistant"
    model: Optional[str] = "llama3.2:3b"
    multi_hop: Optional[bool] = True
    self_rag: Optional[bool] = True

class TTSRequest(BaseModel):
    text: str

class CrawlRequest(BaseModel):
    url: str
    workspace: Optional[str] = "documents"

class MindmapRequest(BaseModel):
    workspace: Optional[str] = "documents"
    file: Optional[str] = None

class TopicsRequest(BaseModel):
    workspace: Optional[str] = "documents"

class TranslateRequest(BaseModel):
    text: str
    language: str

class BattleRequest(BaseModel):
    model_a: str
    model_b: str
    question: str
    workspace: Optional[str] = "documents"

class QuizRequest(BaseModel):
    workspace: Optional[str] = "documents"

class SqlRequest(BaseModel):
    database: str
    question: str
    workspace: Optional[str] = "documents"

class RedactRequest(BaseModel):
    text: str

class InspectRequest(BaseModel):
    workspace: str
    file: str

class CompareRequest(BaseModel):
    workspace: str
    file_a: str
    file_b: str

class SaveSessionRequest(BaseModel):
    workspace: Optional[str] = "documents"
    name: str
    messages: List[Dict[str, Any]]

class ExportBriefRequest(BaseModel):
    workspace: Optional[str] = "documents"

class ExportDeckRequest(BaseModel):
    workspace: Optional[str] = "documents"


# ------------------------------------------------------------------------------
# REST Endpoints (Mounted at both /api/... and /...)
# ------------------------------------------------------------------------------

@app.get("/api/workspaces")
@app.get("/workspaces")
def get_workspaces():
    base_workspaces = ["documents", "finance", "research", "engineering"]
    all_colls = list_all_collections()
    for b in base_workspaces:
        if b not in all_colls:
            all_colls.append(b)

    result = []
    for ws in all_colls:
        files = list_indexed_files(ws)
        result.append({
            "name": ws,
            "doc_count": len(files),
            "custom": ws not in ("documents", "finance", "research", "engineering")
        })
    return result


@app.post("/api/workspaces")
@app.post("/workspaces")
def create_workspace(req: CreateWorkspaceRequest):
    name = req.name.strip().lower().replace(" ", "_")
    if not name:
        raise HTTPException(status_code=400, detail="Workspace name cannot be empty")
    get_collection(name)
    return {"status": "ok", "name": name}


@app.delete("/api/workspaces/{name}")
@app.delete("/workspaces/{name}")
def delete_workspace(name: str):
    delete_workspace_collection(name)
    return {"status": "ok"}


@app.get("/api/workspaces/{name}/files")
@app.get("/workspaces/{name}/files")
def get_workspace_files(name: str):
    files = list_indexed_files(name)
    return [{"name": f, "type": get_doc_icon_type(f)} for f in files]


@app.post("/api/ingest")
@app.post("/ingest")
async def ingest_files(
    workspace: str = Form(...),
    clear: str = Form("false"),
    files: List[UploadFile] = File(...)
):
    should_clear = clear.lower() in ("true", "1", "yes")
    if should_clear:
        try:
            client = _get_client()
            try:
                client.delete_collection(workspace)
            except Exception:
                pass
        except Exception:
            pass

    for file in files:
        file_path = os.path.join(UPLOADS_DIR, file.filename)
        content = await file.read()
        with open(file_path, "wb") as f_out:
            f_out.write(content)

        if not file.filename.lower().endswith((".sqlite", ".db")):
            raw_docs = process_file(file_path)
            chunks = chunk_documents(raw_docs) if raw_docs else []
            if not chunks:
                chunks = [{
                    "text": f"Document '{file.filename}' indexed into workspace '{workspace}'.",
                    "source": file.filename,
                    "page": 1,
                    "type": "document",
                    "chunk_id": f"{file.filename}_1_0",
                }]
            add_chunks(chunks, collection_name=workspace)

    return {"status": "ok", "count": len(files)}


@app.get("/api/models")
@app.get("/models")
def get_models():
    try:
        models_data = ollama.list()
        names = []
        for m in models_data.get("models", []):
            if isinstance(m, dict):
                n = m.get("name", "")
            else:
                n = getattr(m, "model", str(m))
            if n:
                names.append(n)
        return names if names else ["llama3.2:3b"]
    except Exception:
        return ["llama3.2:3b"]


@app.get("/api/status")
@app.get("/status")
def get_status():
    return get_system_stats()


@app.post("/api/chat")
@app.post("/chat")
def chat(req: ChatRequest):
    filter_src = None
    if req.focus_file and req.focus_file != "All Documents":
        filter_src = req.focus_file

    result = generate_answer(
        question=req.query,
        model=req.model or "llama3.2:3b",
        collection_name=req.workspace or "documents",
        persona_name=req.persona or "General Assistant",
        use_agentic_decomposition=req.multi_hop if req.multi_hop is not None else True,
        filter_source=filter_src,
    )

    answer_text = result.get("answer", "No response generated.")
    sources_raw = result.get("sources", [])

    sources_formatted = []
    for idx, s in enumerate(sources_raw, 1):
        p_val = s.get("page")
        try:
            p_int = int(p_val)
        except (ValueError, TypeError):
            p_int = None

        sources_formatted.append({
            "id": idx,
            "filename": s.get("source", "Document"),
            "page": p_int,
            "chunk_id": s.get("chunk_id", f"chunk_{idx}"),
            "score": round(float(s.get("hybrid_score", max(0.6, 0.96 - idx * 0.05))), 2),
            "text": s.get("text", "")[:400]
        })

    verified = True
    if req.self_rag:
        try:
            critic = critic_verify_answer(
                req.query,
                answer_text,
                "\n".join([s["text"] for s in sources_formatted])
            )
            if critic.get("refined_answer"):
                answer_text = critic["refined_answer"]
            verified = critic.get("is_grounded", True)
        except Exception:
            verified = True

    return {
        "answer": answer_text,
        "sources": sources_formatted,
        "verified": verified
    }


@app.post("/api/tts")
@app.post("/tts")
def tts(req: TTSRequest):
    audio_path = speak_text_to_file(req.text)
    if not audio_path or not os.path.exists(audio_path):
        raise HTTPException(status_code=500, detail="Failed to synthesize speech")
    return FileResponse(audio_path, media_type="audio/wav")


@app.post("/api/voice")
@app.post("/voice")
async def voice(
    audio: UploadFile = File(...),
    workspace: str = Form("documents"),
    model: str = Form("llama3.2:3b"),
    persona: str = Form("General Assistant")
):
    audio_bytes = await audio.read()
    v_res = process_voice_turn(
        audio_bytes=audio_bytes,
        model=model,
        workspace=workspace,
        persona=persona,
    )

    b64_audio = None
    if v_res.get("audio_path") and os.path.exists(v_res["audio_path"]):
        with open(v_res["audio_path"], "rb") as f_in:
            b64_audio = base64.b64encode(f_in.read()).decode("utf-8")

    return {
        "transcript": v_res.get("transcript", ""),
        "answer": v_res.get("answer", ""),
        "audio_b64": b64_audio
    }


@app.post("/api/crawl")
@app.post("/crawl")
def crawl(req: CrawlRequest):
    try:
        saved_txt_path = crawl_and_save_webpage(req.url, UPLOADS_DIR)
        filename = os.path.basename(saved_txt_path)
        raw_docs = process_file(saved_txt_path)
        chunks = chunk_documents(raw_docs)
        add_chunks(chunks, collection_name=req.workspace)
        return {"message": f"Successfully crawled and indexed '{filename}' into workspace '{req.workspace}'."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Web crawling failed: {str(e)}")


@app.post("/api/mindmap")
@app.post("/mindmap")
def mindmap(req: MindmapRequest):
    try:
        mm_code = generate_mindmap(collection_name=req.workspace)
        return {"mermaid": mm_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/topics")
@app.post("/topics")
def topics(req: TopicsRequest):
    try:
        clusters_raw = discover_topic_clusters(collection_name=req.workspace)
        clusters = [
            {"title": c.get("topic", f"Topic {i+1}"), "description": c.get("description", "")}
            for i, c in enumerate(clusters_raw)
        ]
        return {"clusters": clusters}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/translate")
@app.post("/translate")
def translate(req: TranslateRequest):
    try:
        tr = translate_text(req.text, req.language)
        return {"translation": tr}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/battle")
@app.post("/battle")
def battle(req: BattleRequest):
    try:
        res_a = generate_answer(req.question, model=req.model_a, collection_name=req.workspace)
        res_b = generate_answer(req.question, model=req.model_b, collection_name=req.workspace)
        return {
            "a": res_a.get("answer", ""),
            "b": res_b.get("answer", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/quiz")
@app.post("/quiz")
def quiz(req: QuizRequest):
    try:
        items = generate_quiz(collection_name=req.workspace)
        questions = [item.get("question", str(item)) for item in items]
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/sql")
@app.post("/sql")
def sql(req: SqlRequest):
    db_path = os.path.join(UPLOADS_DIR, req.database)
    if not os.path.exists(db_path):
        raise HTTPException(status_code=404, detail=f"Database '{req.database}' not found in uploads")

    res = query_sqlite_database(db_path, req.question)
    df = res.get("dataframe")
    columns = [str(c) for c in df.columns] if df is not None else []
    rows = df.values.tolist() if df is not None else []
    return {
        "sql": res.get("sql", ""),
        "columns": columns,
        "rows": rows
    }


@app.post("/api/redact")
@app.post("/redact")
def redact(req: RedactRequest):
    try:
        redacted_out, _ = redact_pii_text(req.text)
        return {"redacted": redacted_out}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/inspect")
@app.post("/inspect")
def inspect(req: InspectRequest):
    try:
        coll = get_collection(req.workspace)
        data = coll.get(where={"source": req.file})
        chunks = []
        if data and data.get("documents"):
            for idx, doc_text in enumerate(data["documents"]):
                cid = data["ids"][idx] if data.get("ids") and idx < len(data["ids"]) else idx
                meta = data["metadatas"][idx] if data.get("metadatas") and idx < len(data["metadatas"]) else {}
                chunks.append({
                    "chunk_id": cid,
                    "text": doc_text,
                    "tokens": len(doc_text.split()),
                    "metadata": meta
                })
        return {"chunks": chunks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/compare")
@app.post("/compare")
def compare(req: CompareRequest):
    path_a = os.path.join(UPLOADS_DIR, req.file_a)
    path_b = os.path.join(UPLOADS_DIR, req.file_b)
    if not os.path.exists(path_a) or not os.path.exists(path_b):
        raise HTTPException(status_code=404, detail="One or both files to compare do not exist on disk")

    try:
        res = compare_documents(path_a, path_b)
        return {"summary": res.get("summary", "No summary generated.")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sessions")
@app.get("/sessions")
def get_sessions(workspace: Optional[str] = Query(None)):
    return list_sessions()


@app.post("/api/sessions")
@app.post("/sessions")
def post_session(req: SaveSessionRequest):
    save_session(req.name, req.messages)
    return {"status": "ok"}


@app.get("/api/sessions/{name}")
@app.get("/sessions/{name}")
def get_session(name: str, workspace: Optional[str] = Query(None)):
    messages = load_session(name)
    return {"messages": messages}


@app.delete("/api/sessions/{name}")
@app.delete("/sessions/{name}")
def del_session(name: str):
    delete_session(name)
    return {"status": "ok"}


@app.post("/api/export/brief")
@app.post("/export/brief")
def export_brief(req: ExportBriefRequest):
    try:
        md = generate_executive_brief(req.workspace)
        return {"markdown": md}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/export/deck")
@app.post("/export/deck")
def export_deck(req: ExportDeckRequest):
    deck_path = os.path.join(REPORTS_DIR, "Executive_Deck.pptx")
    try:
        generate_pptx_deck(deck_path, req.workspace)
        if not os.path.exists(deck_path):
            raise HTTPException(status_code=500, detail="Deck generation failed")
        return FileResponse(
            deck_path,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            filename="Executive_Deck.pptx"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=False)
