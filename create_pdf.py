import os
import csv
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Skip header & footer on title page
            return
        
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header
        self.drawString(54, letter[1] - 36, "File-Integrity Verification Dashboard — Cyber Analyst Submission")
        self.drawRightString(letter[0] - 54, letter[1] - 36, "HCL Internship Project")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
        
        # Footer
        self.line(54, 45, letter[0] - 54, 45)
        self.drawString(54, 32, "ABES Engineering College")
        self.drawRightString(letter[0] - 54, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def generate_pdf():
    pdf_filename = "Project_Submission.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=colors.HexColor('#0f172a'),
        alignment=1, # Center
        spaceAfter=15
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=15,
        leading=20,
        textColor=colors.HexColor('#0284c7'),
        alignment=1,
        spaceAfter=25
    )

    meta_label_style = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#334155'),
        alignment=1
    )

    meta_val_style = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#0f172a'),
        alignment=1,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=10,
        spaceAfter=10
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceAfter=10
    )

    tbl_cell = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#1e293b')
    )

    tbl_header = ParagraphStyle(
        'TblHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    link_style = ParagraphStyle(
        'LinkStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#0284c7')
    )

    story = []

    # ================= PAGE 1: TITLE PAGE =================
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("🛡️ File-Integrity Verification Dashboard", title_style))
    story.append(Paragraph("Cyber Analyst Project | HCL Internship Evaluation", subtitle_style))
    story.append(Spacer(1, 0.4 * inch))
    
    story.append(HRFlowable(width="60%", thickness=1.5, color=colors.HexColor('#0284c7'), spaceAfter=30))
    
    story.append(Paragraph("AUTHOR & SUBMISSION DETAILS", ParagraphStyle('SubSub', parent=meta_label_style, fontSize=12, textColor=colors.HexColor('#64748b'), spaceAfter=15)))
    story.append(Paragraph("Submission Details:", meta_label_style))
    story.append(Paragraph("<b>Not specified</b>", meta_val_style))
    
    story.append(Paragraph("Institution:", meta_label_style))
    story.append(Paragraph("<b>ABES Engineering College</b>", meta_val_style))

    story.append(Paragraph("Project Role & Track:", meta_label_style))
    story.append(Paragraph("Cyber Analyst — HCL", meta_val_style))

    story.append(Paragraph("Scan & Submission Date:", meta_label_style))
    story.append(Paragraph("November 22, 2026 / November 26, 2026", meta_val_style))

    story.append(Spacer(1, 0.5 * inch))
    callout_text = (
        "<b>Core Finding Principle:</b><br/>"
        "<i>\"Hash comparison shows THAT a file changed, not WHETHER it is bad — "
        "match each change to approved change records.\"</i>"
    )
    callout_p = Paragraph(callout_text, ParagraphStyle('Callout', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=15, textColor=colors.HexColor('#0f172a'), alignment=1))
    callout_box = Table([[callout_p]], colWidths=[400])
    callout_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f9ff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#bae6fd')),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(callout_box)
    story.append(PageBreak())

    # ================= PAGE 2: DATASET & AUDIT TABLE =================
    story.append(Paragraph("1. Dataset & Audit Records", h1_style))
    story.append(Paragraph(
        "The file integrity verification mechanism evaluated 7 critical target files across system configurations, documentation, and scripts. "
        "Each record captures the observed filesystem state, baseline cryptographic hash status, change approval reconciliation, assigned risk rating, and forensic findings.",
        body_style
    ))

    # Read CSV
    csv_rows = []
    with open('dataset/fim_results.csv', mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        csv_rows.append([Paragraph(h.replace('_', ' ').upper(), tbl_header) for h in headers])
        for row in reader:
            formatted_row = []
            for idx, cell in enumerate(row):
                # Apply styling depending on column
                cell_text = cell
                if headers[idx] == 'status':
                    if cell == 'OK':
                        cell_text = f"<font color='#059669'><b>{cell}</b></font>"
                    elif cell == 'MODIFIED':
                        cell_text = f"<font color='#d97706'><b>{cell}</b></font>"
                    elif cell == 'DELETED':
                        cell_text = f"<font color='#dc2626'><b>{cell}</b></font>"
                    elif cell == 'ADDED':
                        cell_text = f"<font color='#7c3aed'><b>{cell}</b></font>"
                elif headers[idx] == 'risk_level':
                    if cell == 'High':
                        cell_text = f"<font color='#dc2626'><b>{cell}</b></font>"
                    elif cell == 'Medium':
                        cell_text = f"<font color='#d97706'><b>{cell}</b></font>"
                    elif cell == 'Low':
                        cell_text = f"<font color='#2563eb'><b>{cell}</b></font>"
                    elif cell == 'None':
                        cell_text = f"<font color='#059669'><b>{cell}</b></font>"
                elif headers[idx] == 'file_path':
                    cell_text = f"<code>{cell}</code>"
                elif headers[idx] == 'baseline_hash_prefix':
                    cell_text = f"<code>{cell}</code>"
                
                formatted_row.append(Paragraph(cell_text, tbl_cell))
            csv_rows.append(formatted_row)

    # 504 pt usable width (letter width 612 - 108 margin)
    col_widths = [20, 95, 52, 45, 42, 75, 50, 125]
    table = Table(csv_rows, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(table)
    story.append(Spacer(1, 14))

    story.append(Paragraph("<b>Source Dataset Repository Link:</b>", body_style))
    repo_url = "https://github.com/your-username/CYBER_ANALYST_HCL_TECH.git"
    story.append(Paragraph(f'<link href="{repo_url}">{repo_url}</link>', link_style))
    story.append(PageBreak())

    # ================= PAGE 3+: DASHBOARD VISUALIZATIONS =================
    story.append(Paragraph("2. File-Integrity Verification Dashboard", h1_style))
    story.append(Paragraph(
        "Below is the complete dashboard interface built to monitor and present file integrity alerts. "
        "It features live KPI metrics, status distributions, risk severity matrices, and an integrated audit log.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # Add dashboard_full.png
    full_img_path = 'screenshots/dashboard_full.png'
    if os.path.exists(full_img_path):
        # Usable width: 504pt. Aspect ratio of 1440x950 approx.
        # Height 504 * 900 / 1440 = 315 pt
        story.append(Image(full_img_path, width=500, height=312))
    story.append(Spacer(1, 12))

    story.append(PageBreak())

    # Detailed Charts and Table Section
    story.append(Paragraph("2.1 Detailed Component Views", h1_style))
    story.append(Paragraph("<b>Analytical Visualizations (Status Breakdown & Risk Severity Matrix):</b>", body_style))

    charts_img_path = 'screenshots/dashboard_charts.png'
    if os.path.exists(charts_img_path):
        story.append(Image(charts_img_path, width=500, height=135))
    story.append(Spacer(1, 14))

    story.append(Paragraph("<b>Interactive Audit Table Breakdown:</b>", body_style))
    tbl_img_path = 'screenshots/dashboard_table.png'
    if os.path.exists(tbl_img_path):
        story.append(Image(tbl_img_path, width=500, height=210))
    
    story.append(PageBreak())

    # ================= LAST PAGE: GITHUB REPOSITORY =================
    story.append(Paragraph("3. GitHub Repository & Submission Summary", h1_style))
    story.append(Paragraph(
        "All project deliverables, source datasets, interactive dashboard implementations, and evaluation artifacts "
        "have been pushed and archived within the designated GitHub repository.",
        body_style
    ))
    story.append(Spacer(1, 10))

    repo_box_data = [
        [Paragraph("<b>Project:</b>", tbl_cell), Paragraph("File-Integrity Verification Dashboard (FIM)", tbl_cell)],
        [Paragraph("<b>Contributor:</b>", tbl_cell), Paragraph("ABES Engineering College", tbl_cell)],
        [Paragraph("<b>Organization:</b>", tbl_cell), Paragraph("HCL Internship Submission — Cyber Analyst", tbl_cell)],
        [Paragraph("<b>Repository:</b>", tbl_cell), Paragraph(f'<link href="{repo_url}"><b>{repo_url}</b></link>', link_style)],
        [Paragraph("<b>Deliverables:</b>", tbl_cell), Paragraph("Dataset (CSV/JSON), Single-file Dashboard (HTML/JS), Full-page Screenshots, Formal PDF Report", tbl_cell)],
        [Paragraph("<b>Verification:</b>", tbl_cell), Paragraph("Baseline hash tracking verified, 2 High-Risk threats flagged, 1 Approved change reconciled.", tbl_cell)]
    ]
    repo_box = Table(repo_box_data, colWidths=[100, 390])
    repo_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0284c7')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(repo_box)
    story.append(Spacer(1, 24))

    story.append(Paragraph("<b>Instructions to Verify Deliverables:</b>", body_style))
    instructions_text = (
        "1. <b>Clone the Repository:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>git clone https://github.com/your-username/CYBER_ANALYST_HCL_TECH.git</code><br/><br/>"
        "2. <b>Launch Dashboard:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Open <code>dashboard/index.html</code> in any standard web browser.<br/><br/>"
        "3. <b>Inspect Raw Datasets:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Locate <code>dataset/fim_results.csv</code> and <code>dataset/fim_results.json</code> for data pipeline ingestion."
    )
    story.append(Paragraph(instructions_text, body_style))

    # Build PDF with custom NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print("Project_Submission.pdf generated successfully.")

if __name__ == '__main__':
    generate_pdf()
