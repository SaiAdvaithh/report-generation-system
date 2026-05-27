from app.templates.report_template import ReportTemplate
from datetime import datetime
import pytz   # 🔥 IMPORTANT

class EpicTemplate(ReportTemplate):

    def __init__(self, pdf):
        super().__init__(pdf)

    # ---------- HEADER ----------

    def build_header(self, data):

        self.pdf.add_main_header(
            logo_path=data["logo"],
            company=data["company_name"],
            title="WHO GDP Compliance Report",
            report_id=data["report_id"],
            facility=data["facility_name"],
            address=data["address"],
            generated_on=data["date"]
        )

    # ---------- SCOPE ----------

    def scope_section(self):

        self.pdf.add_section("1. Scope and Purpose")

        self.pdf.add_paragraph(
            "This report documents the environmental monitoring conditions "
            "of the facility in accordance with WHO GDP guidelines. "
            "All telemetry data is collected through automated systems "
            "and validated for compliance."
        )

    # ---------- FACILITY ----------

    def facility_section(self, data):

        self.pdf.add_section("2. Facility Profile")

        table = [
            ["Parameter", "Details"],
            ["Facility Name", data["facility_name"]],
            ["Address", data["address"]],
            ["Compliance Standard", "WHO GDP"],
        ]

        self.pdf.add_facility_table(table)

    # ---------- TELEMETRY ----------

    def telemetry_section(self, telemetry):

        self.pdf.add_section("3. Temperature & Sensor Monitoring")

        table = [
            ["Parameter", "Value"],
            ["Temperature (°C)", round(telemetry.temp, 2) if telemetry.temp else "-"],
            ["Humidity (%)", round(telemetry.humidity, 2) if telemetry.humidity else "-"],
            ["CO2 (ppm)", round(telemetry.co2, 2) if telemetry.co2 else "-"],
            ["NH3 (ppm)", round(telemetry.nh3, 2) if telemetry.nh3 else "-"],
            ["Battery (%)", round(telemetry.battery, 2) if telemetry.battery else "-"],
        ]

        self.pdf.add_table(table)

    # ---------- 🔥 TEMPERATURE LOG (FINAL FIXED) ----------

    def temperature_log_section(self, history):

        self.pdf.add_section("4. Temperature & Sensor Log")

        table = [["Time (IST)", "Temp", "Humidity", "CO2", "NH3", "Battery"]]

        ist = pytz.timezone("Asia/Kolkata")  # 🔥 FORCE IST

        if not history:
            table.append(["No Data", "-", "-", "-", "-", "-"])
        else:
            for row in history:

                utc_time = row.get("time")

                if utc_time:
                    # 🔥 ensure UTC → IST conversion properly
                    if utc_time.tzinfo is None:
                        utc_time = pytz.utc.localize(utc_time)

                    local_time = utc_time.astimezone(ist)

                    formatted_time = local_time.strftime("%d-%m-%Y %H:%M:%S")
                else:
                    formatted_time = "-"

                table.append([
                    formatted_time,
                    round(row.get("temp", 0), 2),
                    round(row.get("humidity", 0), 2),
                    round(row.get("co2", 0), 2),
                    round(row.get("nh3", 0), 2),
                    round(row.get("battery", 0), 2),
                ])

        self.pdf.add_table(table)

    # ---------- 🔥 REPORTING PERIOD (FIXED TIMEZONE) ----------

    def reporting_period_section(self, from_date, to_date):

        self.pdf.add_section("5. Reporting Period")

        ist = pytz.timezone("Asia/Kolkata")

        def convert_to_ist(date_str):
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            return dt.astimezone(ist).strftime("%d-%m-%Y %H:%M")

        table = [
            ["From Date", convert_to_ist(from_date)],
            ["To Date", convert_to_ist(to_date)]
        ]

        self.pdf.add_table(table)

    # ---------- LOCATION ----------

    def location_section(self, telemetry):

        self.pdf.add_section("10. Location Data")

        table = [
            ["Latitude", telemetry.lat],
            ["Longitude", telemetry.lon],
        ]

        self.pdf.add_table(table)

    # ---------- SIGNATURE ----------

    def signature_section(self, data):

        self.pdf.add_section("11. Authorization")

        self.pdf.add_signature_block(
            auditor=data["auditor"],
            reviewer=data["reviewer"],
            approver=data["approver"],
            signature_path=data["signature"]
        )

    # ---------- CHART ----------

    def chart_section(self, chart_path):

        if chart_path:
            self.pdf.add_section("9. Temperature Trend Analysis")
            self.pdf.add_image(chart_path)

    # ---------- STATISTICS  ----------

    def statistics_section(self, stats):

        self.pdf.add_section("6. Temperature Statistics")

        if not stats:
            self.pdf.add_paragraph("No data available")
            return

        table = [
            ["Metric", "Value"],
            ["Minimum Temperature", round(stats["min_temp"], 2)],
            ["Maximum Temperature", round(stats["max_temp"], 2)],
            ["Average Temperature", round(stats["avg_temp"], 2)],
        ]

        self.pdf.add_table(table)

    # ---------- COMPLIANCE  ----------
    def compliance_section(self, temp_status):

        self.pdf.add_section("7. Compliance Status")

        table = [
            ["Parameter", "Status"],
            ["Temperature Compliance", temp_status]
        ]

        self.pdf.add_table(table)

    # ---------- SUMMARY  ----------
    def summary_section(self, summary):

        self.pdf.add_section("8. Final Compliance Summary")

        table = [
            ["Metric", "Result"],
            ["Compliance Score (%)", f"{summary['score']}%"],
            ["Final Status", summary["status"]],
        ]

        self.pdf.add_table(table)

        # 🔥 Conclusion text
        if summary["status"] == "EXCELLENT":
            conclusion = "Facility is fully compliant with WHO GDP standards."
        elif summary["status"] == "SATISFACTORY":
            conclusion = "Facility is mostly compliant but requires minor improvements."
        else:
            conclusion = "Facility is NOT compliant and requires immediate corrective action."

        self.pdf.add_paragraph(f"<b>Conclusion:</b> {conclusion}")