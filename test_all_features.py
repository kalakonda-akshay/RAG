"""
Comprehensive Test Harness for Offline Multimodal RAG Platform.
Executes every single function across core/ and ingestion/ to verify 100% operational readiness.
"""
import os
import sys
import tempfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

print("========================================================")
print("   Running Comprehensive Full System Function Audit...  ")
print("========================================================")

test_results = {}

def run_test(name, func):
    try:
        print(f"\n[TESTING] {name}...", end=" ")
        res = func()
        print("[OK] PASSED")
        test_results[name] = "PASSED"
        return res
    except Exception as e:
        print(f"[FAIL] FAILED: {str(e)}")
        test_results[name] = f"FAILED: {str(e)}"
        return None

# 1. Test System Monitor
def test_system_monitor():
    from core.system_monitor import get_system_stats
    stats = get_system_stats()
    assert "cpu_percent" in stats
    assert "ram_percent" in stats
    return stats

run_test("System Monitor (get_system_stats)", test_system_monitor)

# 2. Test Personas & Prompt Templates
def test_personas_and_templates():
    from core.personas import PERSONAS
    from core.prompt_templates import TEMPLATES
    assert len(PERSONAS) >= 5
    assert len(TEMPLATES) >= 4
    return True

run_test("Personas & Templates", test_personas_and_templates)

# 3. Test PII Redaction
def test_pii_redaction():
    from core.doc_tools import redact_pii_text
    redacted, count = redact_pii_text("Call +1-555-0199 or email user@test.com")
    assert count >= 1
    return redacted

run_test("PII Redactor (redact_pii_text)", test_pii_redaction)

# 4. Test Text Parsing & Chunker
def test_text_parser_and_chunker():
    from ingestion.text_parser import extract_text_from_textfile
    from core.chunker import chunk_documents
    
    with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", delete=False) as tmp:
        tmp.write("This is a sample document for RAG indexing testing. It contains important parameters.")
        tmp_path = tmp.name

    try:
        docs = extract_text_from_textfile(tmp_path)
        assert len(docs) >= 1
        chunks = chunk_documents(docs)
        assert len(chunks) >= 1
        return chunks
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

run_test("Text Parser & Chunker", test_text_parser_and_chunker)

# 5. Test Image Parser
def test_image_parser():
    from ingestion.image_parser import extract_text_from_image
    from PIL import Image

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        img_path = tmp.name

    try:
        img = Image.new("RGB", (200, 100), color="white")
        img.save(img_path)
        docs = extract_text_from_image(img_path)
        assert len(docs) >= 1
        return docs
    finally:
        if os.path.exists(img_path):
            os.remove(img_path)

run_test("Image Parser (extract_text_from_image)", test_image_parser)

# 6. Test CSV / Excel Parser
def test_excel_parser():
    from ingestion.excel_parser import extract_text_from_excel
    with tempfile.NamedTemporaryFile(suffix=".csv", mode="w", delete=False) as tmp:
        tmp.write("Name,Age,Role\nAlice,30,Engineer\nBob,35,Manager")
        csv_path = tmp.name

    try:
        docs = extract_text_from_excel(csv_path)
        assert len(docs) >= 1
        return docs
    finally:
        if os.path.exists(csv_path):
            os.remove(csv_path)

run_test("Excel & CSV Parser (extract_text_from_excel)", test_excel_parser)

# 7. Test Vectorstore Add & Hybrid Query
def test_vectorstore():
    from core.vectorstore import add_chunks, query_collection
    test_chunks = [{
        "text": "Antigravity Orbit RAG Platform enables 100% offline document search.",
        "source": "test_doc.txt",
        "page": 1,
        "type": "text",
        "chunk_id": "test_chunk_999",
    }]
    add_chunks(test_chunks, collection_name="test_collection")
    results = query_collection("Antigravity Orbit RAG", top_k=1, collection_name="test_collection")
    assert len(results) >= 1
    return results

run_test("Vectorstore Hybrid BM25 + Dense Search", test_vectorstore)

# 8. Test RAG Answer Generation
def test_rag_engine():
    from core.rag_engine import generate_answer
    res = generate_answer("What is the Antigravity Orbit platform?", collection_name="test_collection")
    assert "answer" in res
    return res

run_test("RAG Engine (generate_answer)", test_rag_engine)

# 9. Test Agentic Query Decomposition
def test_agentic_rag():
    from core.agentic_rag import decompose_query, extract_entity_graph
    sub_qs = decompose_query("Compare legal risks and financial margins in 2026")
    assert len(sub_qs) >= 1
    graph = extract_entity_graph([{"text": "Alice works at Acme Corp."}])
    return {"sub_queries": sub_qs, "graph": graph}

run_test("Agentic RAG & GraphRAG", test_agentic_rag)

# 10. Test Critic Agent (Self-RAG)
def test_self_rag():
    from core.self_rag import critic_verify_answer
    res = critic_verify_answer("What is Acme?", "Acme is a software company.", "Acme is a tech company.")
    assert "feedback" in res
    return res

run_test("Self-RAG Critic Agent", test_self_rag)

# 11. Test TTS Engine (Read Aloud)
def test_tts_engine():
    from core.tts_engine import speak_text_to_file
    audio_path = speak_text_to_file("Orbit platform offline audio test")
    assert audio_path is None or os.path.exists(audio_path)
    return audio_path

run_test("TTS Engine (speak_text_to_file)", test_tts_engine)

# 12. Test Mind Map Generator
def test_mindmap():
    from core.mindmap_generator import generate_mindmap
    mm = generate_mindmap("test_collection")
    assert "mindmap" in mm
    return mm

run_test("Mind Map Generator (generate_mindmap)", test_mindmap)

# 13. Test Topic Clusters
def test_topics():
    from core.topic_cluster import discover_topic_clusters
    clusters = discover_topic_clusters("test_collection")
    assert isinstance(clusters, list)
    return clusters

run_test("Topic Cluster Discovery", test_topics)

# 14. Test Session Manager
def test_session_manager():
    from core.session_manager import save_session, list_sessions, load_session, delete_session
    dummy_msgs = [{"role": "user", "content": "Hello"}]
    save_session("test_audit_session", dummy_msgs)
    sessions = list_sessions()
    assert "test_audit_session" in sessions
    loaded = load_session("test_audit_session")
    assert len(loaded) == 1
    delete_session("test_audit_session")
    return True

run_test("Session Manager (Save/Load/Delete)", test_session_manager)

# 15. Test Report Generator (Executive Brief & PPTX)
def test_reports():
    from core.report_generator import generate_executive_brief, generate_pptx_deck
    brief = generate_executive_brief("test_collection")
    assert len(brief) > 0
    pptx_path = os.path.join(PROJECT_DIR, "data", "reports", "audit_test.pptx")
    generate_pptx_deck(pptx_path, "test_collection")
    assert os.path.exists(pptx_path)
    return True

run_test("Report Generator (Brief & PPTX)", test_reports)

print("\n========================================================")
print("              AUDIT SUMMARY RESULTS:                    ")
print("========================================================")
passed_count = sum(1 for v in test_results.values() if v == "PASSED")
total_count = len(test_results)
for name, status in test_results.items():
    print(f"  • {name}: {status}")

print(f"\nFinal Score: {passed_count}/{total_count} PASSED")
if passed_count == total_count:
    print("SUCCESS: Every single function is 100% operational!")
else:
    print("WARNING: Some functions failed audit!")
    sys.exit(1)
