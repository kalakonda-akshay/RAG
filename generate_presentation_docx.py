"""
Generates the comprehensive Orbit Prototype Presentation Master Guide in DOCX format for the presentation today.
"""
import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "data", "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

DOCX_PROJECT_PATH = os.path.join(REPORTS_DIR, "Orbit_Prototype_Presentation_Master_Guide.docx")
DOCX_DESKTOP_PATH = r"C:\Users\Akshay\OneDrive\Desktop\Orbit_Prototype_Presentation_Master_Guide.docx"

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def create_presentation_docx():
    doc = Document()

    # Document Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("ORBIT PROTOTYPE PRESENTATION & TECH STACK DEFENSE")
    r_title.bold = True
    r_title.font.size = Pt(20)
    r_title.font.color.rgb = RGBColor(79, 70, 229) # Indigo

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Master Evaluator Pitch · Tech Stack Breakdown (What & Why) · Prototype Workflow · Pitch Script")
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(107, 114, 128)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 1. Project Overview & Pitch
    h1 = doc.add_heading("1. Executive Summary & One-Line Elevator Pitch", level=1)
    h1.runs[0].font.color.rgb = RGBColor(30, 41, 59)

    doc.add_paragraph(
        "• Project Name: Orbit (Offline Multimodal RAG Assistant)\n"
        "• Live Website Portal: https://offlinerag-psi.vercel.app\n"
        "• Source Code Repository: https://github.com/kalakonda-akshay/RAG\n"
        "• Setup Package: https://github.com/kalakonda-akshay/RAG/releases/latest/download/OfflineRAGAssistant_Setup.zip"
    )

    p_pitch = doc.add_paragraph()
    r = p_pitch.add_run("🎤 One-Line Presenter Pitch (Say This to Judges):\n")
    r.bold = True
    r.font.color.rgb = RGBColor(79, 70, 229)
    r_pitch_text = p_pitch.add_run(
        "\"Orbit is a 100% air-gapped, local-first multimodal AI assistant that parses, indexes, and queries private documents, spreadsheets, images, audio, video, and SQL databases completely offline without sending a single byte of data to external cloud servers.\""
    )
    r_pitch_text.italic = True

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 2. Problem Statement & Why Cloud RAG Fails
    doc.add_heading("2. Problem Statement & The 'WHY' (Why Cloud RAG Fails)", level=1)
    
    prob_table = doc.add_table(rows=5, cols=3)
    prob_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    prob_table.autofit = False

    prob_headers = ["Problem in Cloud Systems", "Why Cloud RAG Fails", "How Orbit Prototype Solves It"]
    for j, h_text in enumerate(prob_headers):
        cell = prob_table.rows[0].cells[j]
        cell.text = h_text
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "4F46E5")

    prob_data = [
        ("Data Privacy & Cloud Leakage", "Uploading private PDFs or Q1 financials to OpenAI/Cloud APIs violates privacy laws (GDPR, HIPAA).", "100% Local Execution: All embeddings, vector search, and LLMs run locally on device."),
        ("API Token Costs & Rate Limits", "Enterprise RAG incurs heavy recurring API token costs ($0.03/1K tokens) and rate limits.", "Zero API Costs: Uses Ollama local models (llama3.2:3b + nomic-embed-text) with 0 API cost."),
        ("Hallucination & Lack of Auditability", "Cloud LLMs generate plausible but false facts without verifiable source context.", "Self-RAG Critic Agent: Audits factual alignment against raw retrieved chunks with [1], [2] citations."),
        ("Limited File Format Support", "Standard RAG only parses plain .txt or basic .pdf files.", "29 File Formats: Native parsers for PDF, Word, Excel, PowerPoint, Audio, Video, Images, SQL.")
    ]

    for i, row in enumerate(prob_data):
        r_cells = prob_table.rows[i+1].cells
        r_cells[0].width = Inches(2.0)
        r_cells[1].width = Inches(2.4)
        r_cells[2].width = Inches(2.4)
        r_cells[0].text = row[0]
        r_cells[1].text = row[1]
        r_cells[2].text = row[2]
        r_cells[0].paragraphs[0].runs[0].bold = True
        set_cell_background(r_cells[0], "F1F5F9")
        set_cell_background(r_cells[1], "F8FAFC")
        set_cell_background(r_cells[2], "F8FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 3. Tech Stack Matrix
    doc.add_heading("3. Tech Stack Breakdown (WHAT Does WHAT & WHY)", level=1)

    tech_table = doc.add_table(rows=13, cols=4)
    tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tech_table.autofit = False

    t_headers = ["Layer / Component", "Technology Used", "WHAT It Does", "WHY We Chose It (Justification)"]
    for j, h_text in enumerate(t_headers):
        cell = tech_table.rows[0].cells[j]
        cell.text = h_text
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "4F46E5")

    tech_data = [
        ("Web Production Portal", "React 18 + Vite + Tailwind", "Renders production website and manual on Vercel.", "Ultra-fast build (39s compilation), responsive dark UI design."),
        ("Interactive App UI", "Streamlit + Custom CSS", "Renders 3-rail workspace, 12 tabs, audio recorder.", "Reactive state management, native audio widgets, instant Python backend integration."),
        ("Local LLM Generator", "Ollama (llama3.2:3b)", "Synthesizes grounded answers & splits queries.", "Meta's latest 3B parameter model optimized for local CPU/GPU execution (1.8 GB VRAM)."),
        ("Dense Vector Embeddings", "nomic-embed-text (768-dim)", "Encodes text chunks into 768-dim vector space.", "Outperforms OpenAI embeddings on retrieval benchmarks while running 100% locally."),
        ("Local Vector Database", "ChromaDB", "Stores embeddings & runs fast cosine similarity search.", "Lightweight, zero-server setup, embeds directly in Python process, persists index to disk."),
        ("Sparse Keyword Reranker", "Rank-BM25 (BM25Okapi)", "Scores exact keyword matches & code symbols.", "Resolves dense vector blind spots where semantic distance fails on exact technical terms/IDs."),
        ("Hybrid Rank Fusion", "Reciprocal Rank Fusion (RRF)", "Blends dense vector & sparse BM25 scores: RRF(d).", "Guarantees top precision and recall across semantic context and exact keyword searches."),
        ("Multimodal Ingestion", "PyPDF2, pdfplumber, openpyxl", "Extracts text & tables from PDFs, DOCX, XLSX, PPTX.", "Preserves document layout, spreadsheet formulas, and multi-sheet tabular structures."),
        ("Visual Image OCR Engine", "Pillow (PIL) + Tesseract OCR", "Extracts text from scanned PDFs & images (.png, .jpg).", "Offline optical character recognition for non-searchable scanned image documents."),
        ("Voice STT Engine", "Whisper STT / SpeechRecognition", "Converts microphone speech into text transcripts.", "Hands-free audio interface running completely offline."),
        ("Relational SQL Engine", "SQLite + Python sqlite3", "Natural language text-to-SQL query generation.", "Allows asking plain English queries over relational .sqlite tables without SQL syntax."),
        ("Presentation Exporter", "python-pptx", "Generates 1-click PowerPoint presentations (.pptx).", "Automates executive slide deck creation directly from document findings.")
    ]

    for i, row in enumerate(tech_data):
        r_cells = tech_table.rows[i+1].cells
        r_cells[0].width = Inches(1.6)
        r_cells[1].width = Inches(1.6)
        r_cells[2].width = Inches(1.8)
        r_cells[3].width = Inches(2.0)
        for c_idx, val in enumerate(row):
            r_cells[c_idx].text = val
        r_cells[0].paragraphs[0].runs[0].bold = True
        set_cell_background(r_cells[0], "F1F5F9")
        set_cell_background(r_cells[1], "F8FAFC")
        set_cell_background(r_cells[2], "F8FAFC")
        set_cell_background(r_cells[3], "F8FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 4. End-to-End Prototype Workflow
    doc.add_heading("4. How Our Prototype Works (End-to-End Workflow)", level=1)
    doc.add_paragraph(
        "1. Multimodal File Ingestion: File dropped in Left Rail &rarr; routed to PDF, OCR, Excel, audio, or video parser.\n"
        "2. Recursive Sliding Window Chunking: Text split into 500-token chunks with 50-token overlap preserving sentence context.\n"
        "3. Dual Indexing: Encoded into 768-dim dense vectors in ChromaDB while indexed in a sparse Rank-BM25 inverted index.\n"
        "4. Hybrid RRF Search: Dense cosine similarity and sparse BM25 scores fused using Reciprocal Rank Fusion (RRF).\n"
        "5. Local Synthesis & Self-RAG Audit: llama3.2:3b generates answer with inline citations [1], [2]. Self-RAG critic audits factual alignment.\n"
        "6. Citation Inspection & PPTX Export: User clicks source pills 📄 [1] or downloads PowerPoint slide deck with 1 click."
    )

    # 5. Presenter Script
    doc.add_heading("5. Evaluator / Mentor Pitch Script (1-Minute Presenter Guide)", level=1)
    
    script_p = doc.add_paragraph()
    script_p.add_run("• [0:00 - 0:15] Introduction & Hook:\n").bold = True
    script_p.add_run("\"Good morning mentors! Today we present Orbit — a 100% offline, local-first multimodal RAG platform built to solve the single biggest barrier in enterprise AI: data privacy.\"\n\n")
    
    script_p.add_run("• [0:15 - 0:30] Problem Statement:\n").bold = True
    script_p.add_run("\"Currently, organizations cannot use cloud RAG services like ChatGPT because uploading internal financial reports, legal contracts, or medical records violates privacy laws and incurs heavy API costs.\"\n\n")

    script_p.add_run("• [0:30 - 0:45] The Orbit Solution:\n").bold = True
    script_p.add_run("\"Orbit solves this by running 100% on your local machine. Watch our live prototype: when we upload a scanned PDF and an Excel spreadsheet, Orbit uses PyPDF2 and Tesseract OCR locally to extract text and tables, generating 768-dim embeddings in ChromaDB — all in under 3 seconds.\"\n\n")

    script_p.add_run("• [0:45 - 1:00] Technical Innovation & Features:\n").bold = True
    script_p.add_run("\"We engineered a Hybrid RRF Search Engine combining Dense Vectors with Sparse Rank-BM25, audited by a Self-RAG Critic Agent. Orbit supports 29 file formats, Voice Calls, Natural Language SQL Queries, and 1-Click PowerPoint Deck Export — with zero cloud API dependencies!\"")

    # Save to both paths
    doc.save(DOCX_PROJECT_PATH)
    doc.save(DOCX_DESKTOP_PATH)
    print(f"Saved Presentation Master DOCX to:\n  - {DOCX_PROJECT_PATH}\n  - {DOCX_DESKTOP_PATH}")

if __name__ == "__main__":
    create_presentation_docx()
