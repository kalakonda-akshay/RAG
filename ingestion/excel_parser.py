"""
Handles Excel (.xlsx, .xls) and CSV (.csv) parsing into structured markdown tables.
"""
import os
import pandas as pd


def extract_text_from_excel(file_path: str) -> list[dict]:
    """
    Parses CSV and Excel files into structured text blocks for RAG ingestion.
    Returns a list of dicts: {"text": "<formatted table text>", "source": "<filename>", "page": "<sheet_name>", "type": "spreadsheet"}
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    filename = os.path.basename(file_path)
    _, ext = os.path.splitext(file_path)
    ext_lower = ext.lower()
    results = []

    if ext_lower == ".csv":
        try:
            df = pd.read_csv(file_path)
            if not df.empty:
                # Limit row output if extremely large, convert to markdown string
                md_table = df.head(500).to_markdown(index=False)
                results.append({
                    "text": f"CSV Data Table ({len(df)} rows, {len(df.columns)} columns):\n\n{md_table}",
                    "source": filename,
                    "page": "Sheet 1",
                    "type": "csv",
                })
        except Exception as e:
            # Fallback to plain text read if CSV parsing fails
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read().strip()
                if content:
                    results.append({
                        "text": content,
                        "source": filename,
                        "page": "Sheet 1",
                        "type": "csv",
                    })

    elif ext_lower in [".xlsx", ".xls"]:
        try:
            excel_file = pd.ExcelFile(file_path)
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                if not df.empty:
                    md_table = df.head(500).to_markdown(index=False)
                    results.append({
                        "text": f"Excel Sheet '{sheet_name}' ({len(df)} rows, {len(df.columns)} columns):\n\n{md_table}",
                        "source": filename,
                        "page": sheet_name,
                        "type": "excel",
                    })
        except Exception as e:
            raise RuntimeError(f"Failed to parse Excel file '{filename}': {str(e)}") from e

    return results
