"""
Generates a realistic Financial Analyst sample PDF report and Excel CSV dataset for demoing Orbit's Finance workspace.
"""
import os
import sys

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEMO_DIR = os.path.join(BASE_DIR, "data", "demo")
UPLOADS_DIR = os.path.join(BASE_DIR, "data", "uploads")
DESKTOP_DIR = r"C:\Users\Akshay\OneDrive\Desktop"

os.makedirs(DEMO_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

PDF_PATH = os.path.join(DEMO_DIR, "Q1_2026_Corporate_Financial_Analysis_Report.pdf")
CSV_PATH = os.path.join(DEMO_DIR, "Q1_2026_Segment_Revenue_Breakdown.csv")

def generate_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=4
    )

    sub_style = ParagraphStyle(
        'SubTitleStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=13,
        fontName='Helvetica',
        textColor=colors.HexColor('#64748B'),
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'H1Style',
        parent=styles['Heading2'],
        fontSize=12,
        leading=16,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#4F46E5'),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['BodyText'],
        fontSize=9,
        leading=13,
        fontName='Helvetica',
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    story.append(Paragraph("GLOBAL LOGISTICS & TECH CORP — Q1 2026 FINANCIAL REPORT", title_style))
    story.append(Paragraph("Prepared by Senior Financial Analyst Team | Confidential & Internal Use Only", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=12))

    # Executive Financial Summary
    story.append(Paragraph("1. Executive Summary & Key Performance Indicators (KPIs)", h1_style))
    story.append(Paragraph(
        "Global Logistics & Tech Corp delivered strong first-quarter 2026 financial results, achieving consolidated revenue of <b>$148.5 Million</b> (a 14.2% YoY growth compared to Q1 2025). Gross profit reached <b>$63.5M</b> (42.8% gross margin), while Adjusted EBITDA expanded to <b>$32.4 Million</b> (21.8% EBITDA margin). Net income for the quarter stood at <b>$18.2 Million</b>.", body_style
    ))

    # KPI Table
    kpi_data = [
        [Paragraph("<b>Financial Metric</b>", body_style), Paragraph("<b>Q1 2026 Actual</b>", body_style), Paragraph("<b>Q1 2025 Baseline</b>", body_style), Paragraph("<b>YoY Variance (%)</b>", body_style)],
        [Paragraph("Total Consolidated Revenue", body_style), Paragraph("$148.5M", body_style), Paragraph("$130.0M", body_style), Paragraph("+14.2%", body_style)],
        [Paragraph("Gross Profit", body_style), Paragraph("$63.5M", body_style), Paragraph("$53.3M", body_style), Paragraph("+19.1%", body_style)],
        [Paragraph("Gross Margin (%)", body_style), Paragraph("42.8%", body_style), Paragraph("41.0%", body_style), Paragraph("+180 bps", body_style)],
        [Paragraph("Adjusted EBITDA", body_style), Paragraph("$32.4M", body_style), Paragraph("$26.5M", body_style), Paragraph("+22.2%", body_style)],
        [Paragraph("Net Income", body_style), Paragraph("$18.2M", body_style), Paragraph("$14.8M", body_style), Paragraph("+23.0%", body_style)],
        [Paragraph("Free Cash Flow (FCF)", body_style), Paragraph("$22.6M", body_style), Paragraph("$17.5M", body_style), Paragraph("+29.1%", body_style)],
    ]
    t_kpi = Table(kpi_data, colWidths=[160, 110, 110, 140])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4F46E5')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F8FAFC')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_kpi)
    story.append(Spacer(1, 10))

    # Business Segment Breakdown
    story.append(Paragraph("2. Revenue Breakdown by Business Segment", h1_style))
    story.append(Paragraph(
        "• <b>Enterprise Cloud Solutions</b>: Generated <b>$68.2M</b> (45.9% of total revenue), driven by multi-year SaaS renewals and high enterprise expansion rate.<br/>"
        "• <b>Logistics Automation</b>: Contributed <b>$52.1M</b> (35.1% of revenue), benefiting from new warehouse robotics deployment across North America.<br/>"
        "• <b>Managed Infrastructure Services</b>: Generated <b>$28.2M</b> (19.0% of revenue), providing predictable recurring maintenance cash flow.",
        body_style
    ))

    # Operational & Financial Risk Analysis
    story.append(Paragraph("3. Operational Risk Factors & Compliance Flagging", h1_style))
    story.append(Paragraph(
        "Financial analysis flags three major operational risk factors impacting Q1 operating expense margins:\n<br/>"
        "1. <b>Vendor Concentration Risk</b>: Approximately <b>38% of payment gateway processing</b> is concentrated in a single vendor stack. Any disruption poses immediate revenue processing risk.<br/>"
        "2. <b>Support-Ticket Overhead Inflation</b>: A <b>14% spike in customer support backlog</b> during the March cloud migration increased operational support expenses by $1.4M.<br/>"
        "3. <b>Disaster Recovery Testing Cadence</b>: Audit reveals a <b>testing cadence gap in transaction rollback logs</b> and disaster-recovery database backup verification.",
        body_style
    ))

    # Balance Sheet & Capital Allocation
    story.append(Paragraph("4. Balance Sheet & Capital Liquidity Summary", h1_style))
    story.append(Paragraph(
        "As of March 31, 2026, the company held <b>$84.2 Million</b> in cash and cash equivalents, against <b>$42.0 Million</b> in long-term debt. Working capital remains healthy at <b>$56.8 Million</b>, providing strategic leverage for upcoming R&D investments in autonomous logistics algorithms.", body_style
    ))

    doc.build(story)
    print(f"Generated Financial PDF Report: {PDF_PATH}")

def generate_csv():
    csv_content = """Segment,Q1_2026_Revenue_USD_M,Q1_2025_Revenue_USD_M,YoY_Growth_Pct,Gross_Margin_Pct
Enterprise Cloud Solutions,68.2,58.0,17.6%,54.2%
Logistics Automation,52.1,45.5,14.5%,38.1%
Managed Infrastructure Services,28.2,26.5,6.4%,31.5%
Total Consolidated,148.5,130.0,14.2%,42.8%
"""
    with open(CSV_PATH, "w", encoding="utf-8") as f:
        f.write(csv_content)
    print(f"Generated Financial CSV Dataset: {CSV_PATH}")

if __name__ == "__main__":
    generate_pdf()
    generate_csv()

    # Copy to uploads & desktop for quick access
    import shutil
    shutil.copy2(PDF_PATH, UPLOADS_DIR)
    shutil.copy2(CSV_PATH, UPLOADS_DIR)
    shutil.copy2(PDF_PATH, DESKTOP_DIR)
    shutil.copy2(CSV_PATH, DESKTOP_DIR)
    print("Copied sample financial document directly to Desktop & uploads folder!")
