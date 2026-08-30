"""
FastAPI Local REST API Server for external software integration with the Offline RAG Engine.
"""
import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

from core.rag_engine import generate_answer
from ingestion.router import process_file
from core.chunker import chunk_documents
from core.vectorstore import add_chunks

app = FastAPI(
    title="Offline Multimodal RAG API",
    description="Local REST API for querying and ingesting documents offline.",
    version="1.0.0",
)


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5
    model: str = "llama3.2:3b"
    workspace: str = "documents"


class IngestRequest(BaseModel):
    file_path: str
    workspace: str = "documents"


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok", "service": "Offline Multimodal RAG API"}


@app.post("/api/v1/query")
def query_rag(req: QueryRequest):
    try:
        res = generate_answer(
            question=req.question,
            top_k=req.top_k,
            model=req.model,
            collection_name=req.workspace,
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/ingest")
def ingest_file(req: IngestRequest):
    if not os.path.exists(req.file_path):
        raise HTTPException(status_code=404, detail="File not found")
    try:
        docs = process_file(req.file_path)
        chunks = chunk_documents(docs)
        add_chunks(chunks, collection_name=req.workspace)
        return {
            "status": "success",
            "file": os.path.basename(req.file_path),
            "chunks_indexed": len(chunks),
            "workspace": req.workspace,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
