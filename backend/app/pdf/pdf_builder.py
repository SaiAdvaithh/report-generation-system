from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4


class PDFBuilder:

    def __init__(self, filename):
        self.filename = filename
        self.elements = []
        self.styles = getSampleStyleSheet()

        # Custom styles
        self.title_style = ParagraphStyle(
            name="CustomTitle",
            fontSize=16,
            leading=18,
            spaceAfter=10,
            alignment=1  # center
        )

        self.section_style = ParagraphStyle(
            name="Section",
            fontSize=12,
            leading=14,
            spaceAfter=8,
            spaceBefore=10,
            fontName="Helvetica-Bold"
        )

        self.doc = SimpleDocTemplate(self.filename, pagesize=A4)

    # 🔥 LOGO + HEADER IN SAME ROW
    def add_main_header(self, logo_path, company, title, report_id, facility, address, generated_on):

        logo = Image(logo_path, width=70, height=40) if logo_path else ""

        # 🔥 Title (big + centered feel)
        title_block = Paragraph(
            f"<b>{company}</b><br/>{title}",
            self.title_style
        )

        info_block = Paragraph(
            f"""
            <b>Report ID:</b> {report_id}<br/>
            <b>Facility:</b> {facility}<br/>
            <b>Address:</b> {address}<br/>
            <b>Generated On:</b> {generated_on}
            """,
            self.styles["Normal"]
        )

        table = Table(
            [
                [logo, title_block],
                ["", info_block]
            ],
            colWidths=[80, 420]
        )

        table.setStyle(TableStyle([
            ("SPAN", (1, 0), (1, 0)),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))

        self.elements.append(table)
        self.elements.append(Spacer(1, 20))
    # 🔥 SECTION TITLE
    def add_section(self, title):
        section = Paragraph(f"<b>{title}</b>", self.section_style)
        self.elements.append(section)

    # 🔥 PARAGRAPH
    def add_paragraph(self, text):
        para = Paragraph(text, self.styles["Normal"])
        self.elements.append(para)
        self.elements.append(Spacer(1, 10))

    # 🔥 GENERAL TABLE
    def add_table(self, data):

        table = Table(data, repeatRows=1)

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.whitesmoke, colors.lightgrey])
        ]))

        self.elements.append(table)
        self.elements.append(Spacer(1, 15))

    # 🔥 FACILITY TABLE (LEFT ALIGNED)
    def add_facility_table(self, facility_data):

        table = Table(facility_data, colWidths=[200, 300])

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        self.elements.append(table)
        self.elements.append(Spacer(1, 15))

    # 🔥 TEMPERATURE TABLE (FORMATTED)
    def add_temperature_table(self, telemetry_data):

        table_data = [["Time", "Temp (°C)", "Humidity (%)", "CO2", "NH3", "Battery"]]

        for row in telemetry_data:
            table_data.append([
                str(row.get("time"))[:19],
                round(row.get("temp", 0), 2),
                round(row.get("humidity", 0), 2),
                round(row.get("co2", 0), 2),
                round(row.get("nh3", 0), 2),
                round(row.get("battery", 0), 2),
            ])

        self.add_table(table_data)

    # 🔥 SIGNATURE BLOCK (CLEAN)
    def add_signature_block(self, auditor, reviewer, approver, signature_path):

        self.elements.append(Spacer(1, 40))

        data = [
            ["Prepared By", "Reviewed By", "Approved By"],
            [auditor, reviewer, approver],
            ["", "", ""]
        ]

        table = Table(data, colWidths=[180, 180, 180])

        table.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        self.elements.append(table)

        if signature_path:
            sig = Image(signature_path, width=120, height=50)
            self.elements.append(sig)

    # 🔥 EXTRA IMAGE SUPPORT (for compatibility)
    def add_image(self, image_path, width=100, height=50):
        if image_path:
            img = Image(image_path, width=width, height=height)
            self.elements.append(img)
            self.elements.append(Spacer(1, 10))
            return img

    # 🔥 BUILD
    def build(self):
        self.doc.build(
            self.elements,
            onFirstPage=self.add_footer,
            onLaterPages=self.add_footer
        )
        return self.filename
    # 🔥 FOOTER ()
    def add_footer(self, canvas, doc):
        canvas.saveState()

        footer_text = "CONFIDENTIAL | WHO GDP REPORT"

        canvas.setFont("Helvetica", 8)

        canvas.drawString(30, 20, footer_text)
        canvas.drawRightString(550, 20, f"Page {doc.page}")

        canvas.restoreState()