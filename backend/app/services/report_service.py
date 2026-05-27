from fastapi import HTTPException
import os
import uuid
from datetime import datetime

from app.templates.epic_template import EpicTemplate
from app.pdf.chart_generator import ChartGenerator
from app.pdf.pdf_builder import PDFBuilder
from app.services.statistics_service import StatisticsService
from app.services.compliance_calculator import ComplianceCalculator

class ReportService:

    def __init__(self, repository):
        self.repository = repository

    def generate_container_report(
        self,
        container_id,
        data,
        logo,
        signature,
        from_date,
        to_date
    ):

        if not logo or not signature:
            raise HTTPException(
                status_code=400,
                detail="Logo and signature required"
            )

        # -------- GET DATA --------
        try:
            telemetry = self.repository.get_latest_telemetry(container_id)
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"InfluxDB error: {error}"
            )

        if not telemetry:
            raise HTTPException(
                status_code=404,
                detail="No data found for this container"
            )

        # -------- SAVE FILES --------
        os.makedirs("temp", exist_ok=True)

        logo_path = f"temp/{os.path.basename(logo.filename)}"
        sig_path = f"temp/{os.path.basename(signature.filename)}"

        logo.file.seek(0)
        with open(logo_path, "wb") as f:
            f.write(logo.file.read())

        signature.file.seek(0)
        with open(sig_path, "wb") as f:
            f.write(signature.file.read())

        # -------- CREATE PDF --------
        file_name = f"container_{container_id}_{uuid.uuid4().hex}.pdf"
        pdf = PDFBuilder(file_name)
        template = EpicTemplate(pdf)

        # -------- ADD DATA --------
        data["logo"] = logo_path
        data["signature"] = sig_path
        data["date"] = datetime.now().strftime("%d-%m-%Y")

        # -------- FETCH HISTORY + STATS --------
        try:
            history = self.repository.get_telemetry_by_date_range(
                container_id,
                from_date,
                to_date
            )

            stats_service = StatisticsService()
            stats = stats_service.calculate_temperature_stats(history)

            compliance = ComplianceCalculator()
            temp_status = compliance.evaluate_temperature(telemetry.temp)

            summary = compliance.calculate_score(telemetry)

        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"History fetch error: {error}"
            )

        # -------- CHART --------
        chart_gen = ChartGenerator()
        chart_path = (
            chart_gen.generate_temperature_chart(history)
            if history else None
        )

        # -------- BUILD REPORT --------
        template.build_header(data)
        template.scope_section()
        template.facility_section(data)
        template.telemetry_section(telemetry)
        template.temperature_log_section(history)
        template.reporting_period_section(from_date, to_date)

        template.statistics_section(stats)
        template.compliance_section(temp_status)
        template.summary_section(summary)

        if chart_path:
            template.chart_section(chart_path)

        template.location_section(telemetry)
        template.signature_section(data)

        # -------- BUILD FILE --------
        file = pdf.build()

        # -------- CLEANUP --------
        for path in [logo_path, sig_path, chart_path]:
            if path and os.path.exists(path):
                os.remove(path)

        return {"file": file}
    
'''
    def build_report_data(self, container_id, data, from_date, to_date):
        """
        Prepare data for HTML template.
        """

        # TEMP: reuse existing function
        result = self.generate_container_report(
            container_id,
            data,
            None,
            None,
            from_date,
            to_date
        )

        return result["data"]  # adjust if needed'''