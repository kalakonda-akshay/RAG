"""
Generates the complete Orbit Offline RAG User Guide with embedded screenshots in DOCX and PDF formats.
"""
import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak, HRFlowable
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "reports")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Image paths
IMG_CHAT = os.path.join(BASE_DIR, "offlinerag", "public", "screenshots", "chat_citations.png")
IMG_VOICE = os.path.join(BASE_DIR, "offlinerag", "public", "screenshots", "voice_call.png")
IMG_QUIZ = os.path.join(BASE_DIR, "offlinerag", "public", "screenshots", "quiz_workspace.png")

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def generate_docx():
    docx_path = os.path.join(OUTPUT_DIR, "Orbit_Complete_User_Guide.docx")
    doc = Document()

    # Document Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("ORBIT — OFFLINE MULTIMODAL RAG ASSISTANT\nCOMPLETE USER & INSTALLATION GUIDE")
    r_title.bold = True
    r_title.font.size = Pt(22)
    r_title.font.color.rgb = RGBColor(79, 70, 229) # Indigo

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("100% Air-Gapped Intelligence · Installation · Feature Guide · Screenshot Tour")
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = RGBColor(107, 114, 128)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 1. Executive Summary
    h1 = doc.add_heading("1. Executive Overview & Mission", level=1)
    h1.runs[0].font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph(
        "Orbit is an advanced, local-first Retrieval-Augmented Generation (RAG) platform designed to deliver enterprise-grade document intelligence without sending a single byte of data to external cloud servers. Powered by local vector search, sparse Rank-BM25 recency reranking, and Ollama local LLMs (llama3.2:3b), Orbit ensures complete privacy, zero API costs, and air-gapped security."
    )

    # Key Highlights Table
    table = doc.add_table(rows=4, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    data = [
        ("Platform Name", "Orbit (Offline Multimodal RAG Assistant)"),
        ("Live Website URL", "https://offlinerag-psi.vercel.app"),
        ("Setup Download Package", "https://github.com/kalakonda-akshay/RAG/releases/latest/download/OfflineRAGAssistant_Setup.zip"),
        ("Supported File Formats", "29 Extensions (PDF, Word, Excel, PowerPoint, Audio, Video, Images, SQL)")
    ]

    for i, (k, v) in enumerate(data):
        row = table.rows[i]
        c1, c2 = row.cells[0], row.cells[1]
        c1.width = Inches(2.2)
        c2.width = Inches(4.3)
        c1.text = k
        c2.text = v
        c1.paragraphs[0].runs[0].bold = True
        set_cell_background(c1, "F1F5F9")
        set_cell_background(c2, "F8FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 2. Download & Installation Guide
    doc.add_heading("2. Download & Installation Step-by-Step Guide", level=1)

    p_step1 = doc.add_paragraph()
    r = p_step1.add_run("Step 1: Download the Application Package\n")
    r.bold = True
    p_step1.add_run(
        "Visit the live production web portal at https://offlinerag-psi.vercel.app or download the 1.9 GB standalone setup zip directly from GitHub Releases:\n"
        "Download URL: https://github.com/kalakonda-akshay/RAG/releases/latest/download/OfflineRAGAssistant_Setup.zip\n"
        "Saved File: OfflineRAGAssistant_Setup.zip (1.9 GB)"
    )

    p_step2 = doc.add_paragraph()
    r = p_step2.add_run("\nStep 2: Extract & First-Run Environment Setup\n")
    r.bold = True
    p_step2.add_run(
        "1. Extract OfflineRAGAssistant_Setup.zip to your desired folder (e.g. C:\\OrbitAssistant).\n"
        "2. Open Windows Command Prompt or PowerShell inside the extracted folder.\n"
        "3. Run the automatic setup wizard:\n"
        "   python launcher/first_run_setup.py\n"
        "This script verifies your Python environment, installs core dependencies, and configures Ollama."
    )

    p_step3 = doc.add_paragraph()
    r = p_step3.add_run("\nStep 3: Download Local AI Models (Ollama)\n")
    r.bold = True
    p_step3.add_run(
        "Ensure Ollama is running in the background, then pull the local generation & embedding models:\n"
        "   ollama pull llama3.2:3b\n"
        "   ollama pull nomic-embed-text"
    )

    p_step4 = doc.add_paragraph()
    r = p_step4.add_run("\nStep 4: Launch the Orbit User Interface\n")
    r.bold = True
    p_step4.add_run(
        "Run the launcher script to open the 3-column interactive workspace in your web browser:\n"
        "   python launcher/run_app.py\n"
        "Access URL: http://localhost:8501"
    )

    # 3. Screenshots & Visual Interface Tour
    doc.add_heading("3. Visual Interface & Screenshot Tour", level=1)
    doc.add_paragraph("Below are live screenshots of Orbit running in real-world scenarios:")

    # Screenshot 1
    doc.add_heading("Figure 1: Grounded Q&A Thread & Interactive Citations", level=2)
    doc.add_paragraph("Shows the central Q&A chat stream with numbered citation chips [1], [2], interactive source buttons, and raw text chunk inspector:")
    if os.path.exists(IMG_CHAT):
        doc.add_picture(IMG_CHAT, width=Inches(6.0))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Screenshot 2
    doc.add_heading("Figure 2: Real-Time Voice Call Mode", level=2)
    doc.add_paragraph("Shows real-time microphone audio recording and local Whisper speech-to-text transcription:")
    if os.path.exists(IMG_VOICE):
        doc.add_picture(IMG_VOICE, width=Inches(6.0))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Screenshot 3
    doc.add_heading("Figure 3: Auto-Generated Document Quiz Workspace", level=2)
    doc.add_paragraph("Shows dynamic multiple-choice test questions auto-generated from indexed document contents:")
    if os.path.exists(IMG_QUIZ):
        doc.add_picture(IMG_QUIZ, width=Inches(6.0))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 4. Complete Feature Reference
    doc.add_heading("4. Complete Feature & Workspace Reference (12 Tabs)", level=1)

    features = [
        ("💬 Grounded Q&A Chat", "Dense vector search + Rank-BM25 hybrid retrieval + Self-RAG hallucination verification."),
        ("🎙️ Voice Call Mode", "Hands-free voice interface using microphone input and local Whisper speech transcription."),
        ("🌐 Web Archiver", "Parses and indexes offline web pages, documentation HTML, and articles."),
        ("🗺️ Mind Map Generator", "Generates interactive visual Mermaid.js mind maps from uploaded document concepts."),
        ("🧩 Topic Cluster Discovery", "Performs K-Means semantic clustering to discover hidden themes across files."),
        ("🌐 Multilingual Translator", "Translates document passages into 10+ target languages completely offline."),
        ("⚔️ Model Battle Mode", "Compares responses side-by-side across multiple local LLMs."),
        ("🎓 Auto Document Quiz", "Generates practice test questions with answer keys from document text."),
        ("🗄️ Natural Language SQL Engine", "Queries SQLite (.db/.sqlite) tables using auto-generated SQL code."),
        ("🛡️ PII Redactor & PDF Exporter", "Detects and redacts SSNs, credit cards, emails, and phone numbers, exporting sanitized PDFs."),
        ("🔍 Document Comparator", "Compares two documents side-by-side highlighting overlaps, diffs, and contradictions."),
        ("📊 Report & PPTX Exporter", "Generates 1-click PowerPoint presentations (.pptx) and executive brief summaries.")
    ]

    for f_title, f_desc in features:
        p = doc.add_paragraph()
        r1 = p.add_run(f"{f_title}: ")
        r1.bold = True
        r1.font.color.rgb = RGBColor(79, 70, 229)
        p.add_run(f_desc)

    # 5. 29 File Formats Reference
    doc.add_heading("5. Supported File Formats (29 Extensions)", level=1)
    doc.add_paragraph(
        "• Documents & Presentations (5): .pdf, .docx, .pptx, .ppt, .md\n"
        "• Spreadsheets & Tables (3): .xlsx, .xls, .csv\n"
        "• Image & OCR (7): .png, .jpg, .jpeg, .webp, .bmp, .tiff, .gif\n"
        "• Audio Recordings (3): .wav, .mp3, .m4a\n"
        "• Video Files (4): .mp4, .mkv, .mov, .avi\n"
        "• Code & Text Markup (7): .txt, .py, .js, .json, .html, .xml, .sql\n"
        "• Relational DBs (2): .sqlite, .db"
    )

    doc.save(docx_path)
    print(f"Saved DOCX User Guide to: {docx_path}")

def generate_pdf():
    pdf_path = os.path.join(OUTPUT_DIR, "Orbit_Complete_User_Guide.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#4F46E5'),
        alignment=1,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'SubTitleStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#475569'),
        alignment=1,
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'H1Style',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=15,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['BodyText'],
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    bold_body_style = ParagraphStyle(
        'BoldBodyStyle',
        parent=body_style,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#4F46E5')
    )

    # Title Banner
    story.append(Paragraph("ORBIT — OFFLINE MULTIMODAL RAG ASSISTANT", title_style))
    story.append(Paragraph("COMPLETE USER MANUAL, INSTALLATION & FEATURE GUIDE", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=15))

    # Executive Overview
    story.append(Paragraph("1. Executive Overview & Mission", h1_style))
    story.append(Paragraph(
        "<b>Orbit</b> is an air-gapped, local-first Retrieval-Augmented Generation (RAG) platform. It provides instant semantic Q&A, voice conversations, document quizzes, mind maps, and report generation over private documents without sending any data to cloud services.", body_style
    ))

    # Table
    table_data = [
        [Paragraph("<b>Platform Name</b>", body_style), Paragraph("Orbit (Offline Multimodal RAG Assistant)", body_style)],
        [Paragraph("<b>Live Website Portal</b>", body_style), Paragraph("https://offlinerag-psi.vercel.app", body_style)],
        [Paragraph("<b>Direct Download Link</b>", body_style), Paragraph("https://github.com/kalakonda-akshay/RAG/releases/latest/download/OfflineRAGAssistant_Setup.zip", body_style)],
        [Paragraph("<b>Supported Formats</b>", body_style), Paragraph("29 Extensions (PDF, Word, Excel, PPTX, Audio, Video, Images, SQL)", body_style)]
    ]
    t = Table(table_data, colWidths=[140, 380])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#F1F5F9')),
        ('BACKGROUND', (1,0), (1,-1), colors.HexColor('#F8FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    # Installation Guide
    story.append(Paragraph("2. Download & Installation Step-by-Step Guide", h1_style))
    story.append(Paragraph("<b>Step 1: Download Setup Package</b>", bold_body_style))
    story.append(Paragraph("Download <i>OfflineRAGAssistant_Setup.zip</i> (1.9 GB) from <font color='#4F46E5'><u>https://offlinerag-psi.vercel.app</u></font> or directly from GitHub Releases.", body_style))

    story.append(Paragraph("<b>Step 2: Extract & Environment Setup</b>", bold_body_style))
    story.append(Paragraph("Extract the zip archive and run the setup script: <i>python launcher/first_run_setup.py</i>", body_style))

    story.append(Paragraph("<b>Step 3: Pull Local LLM & Embedding Models</b>", bold_body_style))
    story.append(Paragraph("Run in terminal: <i>ollama pull llama3.2:3b</i> and <i>ollama pull nomic-embed-text</i>", body_style))

    story.append(Paragraph("<b>Step 4: Launch Web Interface</b>", bold_body_style))
    story.append(Paragraph("Start Orbit: <i>python launcher/run_app.py</i> &rarr; Open browser at <b>http://localhost:8501</b>", body_style))
    story.append(Spacer(1, 15))

    # Screenshots Tour
    story.append(Paragraph("3. Visual Screenshot Tour", h1_style))

    if os.path.exists(IMG_CHAT):
        story.append(Paragraph("<b>Figure 1: Grounded Q&A Thread & Interactive Citations</b>", bold_body_style))
        story.append(RLImage(IMG_CHAT, width=520, height=292))
        story.append(Spacer(1, 10))

    if os.path.exists(IMG_VOICE):
        story.append(Paragraph("<b>Figure 2: Real-Time Voice Call Mode</b>", bold_body_style))
        story.append(RLImage(IMG_VOICE, width=520, height=292))
        story.append(Spacer(1, 10))

    if os.path.exists(IMG_QUIZ):
        story.append(Paragraph("<b>Figure 3: Auto-Generated Document Quiz Workspace</b>", bold_body_style))
        story.append(RLImage(IMG_QUIZ, width=520, height=292))
        story.append(Spacer(1, 10))

    # Feature List
    story.append(Paragraph("4. Complete Feature Reference (12 Tabs)", h1_style))
    features = [
        ("💬 Grounded Q&A Chat", "Dense vector search + Rank-BM25 hybrid retrieval + Self-RAG verification."),
        ("🎙️ Voice Call Mode", "Real-time microphone recording and Whisper speech transcription."),
        ("🌐 Web Archiver", "Parses and indexes offline web pages and documentation HTML."),
        ("🗺️ Mind Map Generator", "Generates visual Mermaid.js mind maps from document concepts."),
        ("🧩 Topic Cluster Discovery", "Performs K-Means semantic clustering across document text."),
        ("🌐 Multilingual Translator", "Translates document passages into 10+ target languages offline."),
        ("⚔️ Model Battle Mode", "Compares responses side-by-side across multiple local LLMs."),
        ("🎓 Auto Document Quiz", "Generates practice test questions with answer keys."),
        ("🗄️ Natural Language SQL Engine", "Queries SQLite (.db/.sqlite) tables using auto-generated SQL."),
        ("🛡️ PII Redactor & PDF Exporter", "Redacts SSNs, credit cards, emails, and exports sanitized PDFs."),
        ("🔍 Document Comparator", "Side-by-side comparison of two documents highlighting diffs."),
        ("📊 Report & PPTX Exporter", "1-click PowerPoint presentations (.pptx) and executive brief summaries.")
    ]
    for title, desc in features:
        story.append(Paragraph(f"<b>{title}</b>: {desc}", body_style))

    doc.build(story)
    print(f"Saved PDF User Guide to: {pdf_path}")

if __name__ == "__main__":
    generate_docx()
    generate_pdf()
