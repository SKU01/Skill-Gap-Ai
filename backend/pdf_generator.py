import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print 'Page X of Y' and header/footer."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        # Top banner line
        self.setStrokeColor(colors.HexColor("#2563eb"))
        self.setLineWidth(3)
        self.line(40, letter[1] - 30, letter[0] - 40, letter[1] - 30)

        # Footer divider and text
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.75)
        self.line(40, 42, letter[0] - 40, 42)

        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#2563eb"))
        self.drawString(40, 28, "SkillPath AI")

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(98, 28, "· Confidential Career Readiness & Skill Gap Report")

        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 40, 28, page_str)
        self.restoreState()


def create_report_pdf(student_data, report_data):
    """
    Generates a PDF Skill Gap Analysis Report as bytes.
    student_data: dict with name, email, branch, year (optional)
    report_data: dict returned by /api/analyze:
      {
        'role': 'Full Stack Developer',
        'marks': '85',
        'extracted_skills': [...],
        'report': [
          {'skill':'Python', 'category':'Backend', 'current':40, 'required':80, 'gap':40, 'weight':1.2, 'score':48.0, ...}
        ],
        'recommendations': [
          {'title':..., 'provider':..., 'level':..., 'url':...}
        ],
        'note': '...'
      }
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=46,
        bottomMargin=54
    )

    usable_width = letter[0] - 80 # 612 - 80 = 532 pt

    # Base stylesheet
    styles = getSampleStyleSheet()

    # Custom styles
    brand_style = ParagraphStyle(
        "BrandStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1e3a8a")
    )
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0f172a")
    )
    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#64748b")
    )
    meta_style = ParagraphStyle(
        "MetaText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#475569")
    )
    meta_bold = ParagraphStyle(
        "MetaTextBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#0f172a")
    )
    section_h2 = ParagraphStyle(
        "SectionH2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=10,
        spaceAfter=6
    )
    section_desc = ParagraphStyle(
        "SectionDesc",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=8
    )
    tbl_header = ParagraphStyle(
        "TblHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=0
    )
    tbl_cell = ParagraphStyle(
        "TblCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1e293b")
    )
    tbl_cell_bold = ParagraphStyle(
        "TblCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0f172a")
    )
    tbl_cell_center = ParagraphStyle(
        "TblCellCenter",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#334155"),
        alignment=1
    )
    badge_met = ParagraphStyle(
        "BadgeMet",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#15803d"),
        alignment=1
    )
    badge_gap = ParagraphStyle(
        "BadgeGap",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#b91c1c"),
        alignment=1
    )
    note_text = ParagraphStyle(
        "NoteText",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#475569")
    )

    story = []

    # 1. Header Section
    role_name = report_data.get("role", "Target Role")
    student_name = student_data.get("name", "Student")
    student_email = student_data.get("email", "")
    gen_time = datetime.now().strftime("%B %d, %Y · %I:%M %p")

    header_left = [
        Paragraph("SkillPath <b>AI</b>", brand_style),
        Spacer(1, 2),
        Paragraph("AI-Powered Career Readiness & Skill Gap Analysis", subtitle_style),
    ]
    header_right = [
        Paragraph(f"<b>Report Generated:</b> {gen_time}", meta_style),
        Paragraph("<b>Assessment Type:</b> Resume & Role Alignment", meta_style),
    ]

    header_table = Table(
        [[header_left, header_right]],
        colWidths=[usable_width * 0.6, usable_width * 0.4]
    )
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceBefore=0, spaceAfter=10))

    # 2. Student & Assessment Profile Card
    marks_str = str(report_data.get("marks") or "").strip()
    marks_val = f"{marks_str}%" if marks_str else "Not specified"

    profile_data = [
        [
            Paragraph("<b>Candidate Name:</b>", meta_bold),
            Paragraph(student_name, meta_style),
            Paragraph("<b>Target Role:</b>", meta_bold),
            Paragraph(f"<b>{role_name}</b>", ParagraphStyle("RoleHighlight", parent=meta_bold, textColor=colors.HexColor("#1d4ed8"))),
        ],
        [
            Paragraph("<b>Email:</b>", meta_bold),
            Paragraph(student_email or "N/A", meta_style),
            Paragraph("<b>Academic Marks:</b>", meta_bold),
            Paragraph(marks_val, meta_style),
        ]
    ]

    profile_table = Table(
        profile_data,
        colWidths=[usable_width * 0.22, usable_width * 0.28, usable_width * 0.22, usable_width * 0.28]
    )
    profile_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(profile_table)
    story.append(Spacer(1, 12))

    # 3. KPI Summary Metrics
    skills_list = report_data.get("report", [])
    extracted_skills = report_data.get("extracted_skills", [])
    total_evaluated = len(skills_list)
    total_detected = len(extracted_skills)
    total_gaps = sum(1 for s in skills_list if s.get("gap", 0) > 0)
    total_met = total_evaluated - total_gaps
    readiness_pct = int(round((total_met / total_evaluated * 100))) if total_evaluated > 0 else 0

    kpi_cols = [
        [
            Paragraph(f"<font size=18 color='#2563eb'><b>{total_detected}</b></font>", ParagraphStyle("KpiNum", alignment=1)),
            Paragraph("<font color='#64748b' size=7.5>Skills Detected in Resume</font>", ParagraphStyle("KpiLbl", alignment=1))
        ],
        [
            Paragraph(f"<font size=18 color='#0f172a'><b>{total_evaluated}</b></font>", ParagraphStyle("KpiNum", alignment=1)),
            Paragraph("<font color='#64748b' size=7.5>Required Skills Evaluated</font>", ParagraphStyle("KpiLbl", alignment=1))
        ],
        [
            Paragraph(f"<font size=18 color='#ea580c'><b>{total_gaps}</b></font>", ParagraphStyle("KpiNum", alignment=1)),
            Paragraph("<font color='#64748b' size=7.5>Skills Needing Growth</font>", ParagraphStyle("KpiLbl", alignment=1))
        ],
        [
            Paragraph(f"<font size=18 color='#16a34a'><b>{readiness_pct}%</b></font>", ParagraphStyle("KpiNum", alignment=1)),
            Paragraph("<font color='#64748b' size=7.5>Role Readiness Fit</font>", ParagraphStyle("KpiLbl", alignment=1))
        ]
    ]

    kpi_table = Table([kpi_cols], colWidths=[usable_width / 4.0] * 4)
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 14))

    # 4. Detailed Skill Gap Breakdown Table
    story.append(Paragraph("1. Current vs. Required Skill Gap Breakdown", section_h2))
    story.append(Paragraph("Evaluates competencies against target role benchmarks on a 0–100 scale.", section_desc))

    tbl_data = [[
        Paragraph("Skill Name", tbl_header),
        Paragraph("Category", tbl_header),
        Paragraph("Current", tbl_header),
        Paragraph("Required", tbl_header),
        Paragraph("Gap", tbl_header),
        Paragraph("Priority", tbl_header),
        Paragraph("Status", tbl_header),
    ]]

    for i, s in enumerate(skills_list):
        current_val = int(s.get("current", 0))
        required_val = int(s.get("required", 0))
        gap_val = int(s.get("gap", 0))
        score_val = s.get("score", 0)

        if gap_val == 0:
            status_p = Paragraph("✔ Met", badge_met)
        else:
            status_p = Paragraph(f"▲ Gap (-{gap_val})", badge_gap)

        tbl_data.append([
            Paragraph(str(s.get("skill", "")), tbl_cell_bold),
            Paragraph(str(s.get("category", "")), tbl_cell),
            Paragraph(f"{current_val}%", tbl_cell_center),
            Paragraph(f"{required_val}%", tbl_cell_center),
            Paragraph(f"{gap_val}", tbl_cell_center),
            Paragraph(f"{score_val}", tbl_cell_center),
            status_p
        ])

    col_widths = [
        usable_width * 0.28, # Skill
        usable_width * 0.22, # Category
        usable_width * 0.10, # Current
        usable_width * 0.10, # Required
        usable_width * 0.08, # Gap
        usable_width * 0.10, # Priority
        usable_width * 0.12  # Status
    ]

    skills_table = Table(tbl_data, colWidths=col_widths, repeatRows=1)
    t_style = [
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e3a8a")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,0), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ]

    # Alternating row colors
    for row_idx in range(1, len(tbl_data)):
        if row_idx % 2 == 0:
            t_style.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor("#f8fafc")))
        else:
            t_style.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor("#ffffff")))

    skills_table.setStyle(TableStyle(t_style))
    story.append(skills_table)
    story.append(Spacer(1, 14))

    # 5. Top Priority Focus Areas
    gap_skills = [s for s in skills_list if s.get("gap", 0) > 0]
    if gap_skills:
        story.append(Paragraph("2. Top Priority Learning Areas", section_h2))
        story.append(Paragraph("Ranked by weighted gap impact — focus on these areas first to maximize career readiness.", section_desc))

        priority_rows = [[
            Paragraph("Rank", tbl_header),
            Paragraph("Priority Skill", tbl_header),
            Paragraph("Current Level", tbl_header),
            Paragraph("Target Level", tbl_header),
            Paragraph("Gap Points", tbl_header),
            Paragraph("Impact Score", tbl_header),
        ]]

        for rank, s in enumerate(gap_skills[:5], start=1):
            priority_rows.append([
                Paragraph(f"<b>#{rank}</b>", tbl_cell_center),
                Paragraph(f"<b>{s.get('skill','')}</b> <font size=7.5 color='#64748b'>({s.get('category','')})</font>", tbl_cell),
                Paragraph(f"{s.get('current',0)}%", tbl_cell_center),
                Paragraph(f"{s.get('required',0)}%", tbl_cell_center),
                Paragraph(f"{s.get('gap',0)}", tbl_cell_center),
                Paragraph(f"<b>{s.get('score',0)} pts</b>", tbl_cell_center),
            ])

        priority_col_widths = [
            usable_width * 0.08,
            usable_width * 0.44,
            usable_width * 0.12,
            usable_width * 0.12,
            usable_width * 0.12,
            usable_width * 0.12
        ]
        priority_table = Table(priority_rows, colWidths=priority_col_widths, repeatRows=1)
        p_style = [
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2563eb")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 4.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ]
        for row_idx in range(1, len(priority_rows)):
            if row_idx % 2 == 0:
                p_style.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor("#f8fafc")))
            else:
                p_style.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor("#ffffff")))
        priority_table.setStyle(TableStyle(p_style))
        story.append(priority_table)
        story.append(Spacer(1, 14))

    # 6. Recommended Learning Courses
    recommendations = report_data.get("recommendations", [])
    if recommendations:
        story.append(Paragraph("3. Recommended Learning Resources & Courses", section_h2))
        story.append(Paragraph("Curated educational resources specifically selected to bridge your identified skill gaps.", section_desc))

        rec_rows = [[
            Paragraph("Course / Resource Title", tbl_header),
            Paragraph("Provider", tbl_header),
            Paragraph("Level", tbl_header),
            Paragraph("Link", tbl_header),
        ]]

        for c in recommendations:
            url = c.get("url", "#")
            link_html = f'<a href="{url}" color="#2563eb"><u>Open Course ↗</u></a>' if url and url != "#" else "Online Course"
            rec_rows.append([
                Paragraph(f"<b>{c.get('title','')}</b>", tbl_cell),
                Paragraph(c.get("provider", "Online"), tbl_cell),
                Paragraph(c.get("level", "All Levels"), tbl_cell_center),
                Paragraph(link_html, tbl_cell_center),
            ])

        rec_col_widths = [
            usable_width * 0.50,
            usable_width * 0.22,
            usable_width * 0.14,
            usable_width * 0.14
        ]
        rec_table = Table(rec_rows, colWidths=rec_col_widths, repeatRows=1)
        r_style = [
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f766e")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 4.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ]
        for row_idx in range(1, len(rec_rows)):
            if row_idx % 2 == 0:
                r_style.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor("#f8fafc")))
            else:
                r_style.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor("#ffffff")))
        rec_table.setStyle(TableStyle(r_style))
        story.append(rec_table)
        story.append(Spacer(1, 14))

    # 7. Note / Disclaimer Box
    note_msg = report_data.get("note", "Resume detection indicates skill presence only. Review and adjust self-ratings for a more accurate proficiency estimate.")
    notice_table = Table(
        [[
            Paragraph("<b>Assessment Advisory:</b> " + note_msg, note_text)
        ]],
        colWidths=[usable_width]
    )
    notice_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#eff6ff")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#bfdbfe")),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 9),
        ('RIGHTPADDING', (0,0), (-1,-1), 9),
    ]))
    story.append(KeepTogether([notice_table]))

    doc.build(story, canvasmaker=NumberedCanvas)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
