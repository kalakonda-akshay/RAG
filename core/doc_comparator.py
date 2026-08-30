"""
Automated Document Comparison and Clause Redlining engine.
"""
import os
import difflib
import ollama

try:
    from ingestion.router import process_file
except ImportError:
    from router import process_file


def compare_documents(file1_path: str, file2_path: str) -> dict:
    """
    Parses two documents, computes line-by-line diffs, and synthesizes a clause comparison and risk report.
    Returns: {"summary": "<LLM summary>", "diff_lines": [...], "file1": "<name>", "file2": "<name>"}
    """
    if not os.path.exists(file1_path) or not os.path.exists(file2_path):
        raise FileNotFoundError("One or both files to compare do not exist.")

    f1_name = os.path.basename(file1_path)
    f2_name = os.path.basename(file2_path)

    docs1 = process_file(file1_path)
    docs2 = process_file(file2_path)

    text1 = "\n".join([d.get("text", "") for d in docs1])
    text2 = "\n".join([d.get("text", "") for d in docs2])

    lines1 = text1.splitlines()
    lines2 = text2.splitlines()

    # Compute unified diff
    diff_gen = list(difflib.unified_diff(lines1, lines2, fromfile=f1_name, tofile=f2_name, lineterm=""))

    # Synthesize AI comparison summary
    prompt = f"""Compare the following two documents and provide a structured comparison report:
# Document Comparison Report
## 1. Key Additions in {f2_name}
## 2. Key Deletions from {f1_name}
## 3. Numerical & Financial Differences
## 4. Legal / Operational Risk Analysis

Document 1 ({f1_name}):
{text1[:1500]}

Document 2 ({f2_name}):
{text2[:1500]}

Report:"""

    try:
        res = ollama.generate(model="llama3.2:3b", prompt=prompt)
        summary_report = res.get("response", "Could not generate comparison report.").strip()
    except Exception as e:
        summary_report = f"Diff calculated ({len(diff_gen)} lines changed). Could not generate LLM comparison: {str(e)}"

    return {
        "file1": f1_name,
        "file2": f2_name,
        "summary": summary_report,
        "diff_lines": diff_gen[:100],
    }
