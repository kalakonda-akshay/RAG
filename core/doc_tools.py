"""
Automatic PII Redaction and Offline PDF Management Tools.
"""
import os
import re
import pymupdf as fitz


def redact_pii_text(text: str) -> tuple[str, int]:
    """
    Redacts sensitive Personally Identifiable Information (Emails, Phone numbers, SSNs, Credit Cards)
    from text using regex patterns.
    Returns (redacted_text, count_of_redactions).
    """
    if not text:
        return "", 0

    redactions_count = 0

    # Patterns
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
    ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
    card_pattern = r'\b(?:\d[ -]*?){13,16}\b'

    cleaned_text, count_e = re.subn(email_pattern, "[REDACTED-EMAIL]", text)
    cleaned_text, count_p = re.subn(phone_pattern, "[REDACTED-PHONE]", cleaned_text)
    cleaned_text, count_s = re.subn(ssn_pattern, "[REDACTED-SSN]", cleaned_text)
    cleaned_text, count_c = re.subn(card_pattern, "[REDACTED-CARD]", cleaned_text)

    total_redactions = count_e + count_p + count_s + count_c
    return cleaned_text, total_redactions


def merge_pdf_files(pdf_paths: list[str], output_path: str) -> str:
    """
    Merges multiple PDF files into a single merged PDF file.
    Returns path to the output PDF.
    """
    merged_doc = fitz.open()
    for path in pdf_paths:
        if os.path.exists(path):
            doc = fitz.open(path)
            merged_doc.insert_pdf(doc)
            doc.close()

    merged_doc.save(output_path)
    merged_doc.close()
    return output_path
