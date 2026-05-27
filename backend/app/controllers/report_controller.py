from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
import os
from datetime import datetime

from app.services.report_service import ReportService
from app.repository.influx_repository import InfluxRepository

from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
import pdfkit
#from app.services.report_service import get_report_data

router = APIRouter()

repository = InfluxRepository(
    url="http://localhost:8086",
    token="Z0Kb68SfFxT-gsYd-5pO6uKIDhIHNEh5qu-hQAVUMt9HGNRHuv9wmaEV5yxDWoZEaVEhzN1LtS-etggZQOnO1w==",
    org="Epic Logic Solutions",
    bucket="hardware_data"
)

report_service = ReportService(repository)


@router.post("/report/{container_id}")
def generate_report(
    container_id: str,
    company_name: str = Form(...),
    facility_name: str = Form(...),
    address: str = Form(...),
    report_id: str = Form(...),
    auditor: str = Form(...),
    reviewer: str = Form(...),
    approver: str = Form(...),

    from_date: str = Form(...),
    to_date: str = Form(...),

    logo: UploadFile = File(...),
    signature: UploadFile = File(...)

    

):


    # -------- PREPARE DATA --------
    data = {
        "company_name": company_name,
        "facility_name": facility_name,
        "address": address,
        "report_id": report_id,
        "auditor": auditor,
        "reviewer": reviewer,
        "approver": approver
    }

    # -------- GENERATE REPORT --------
    result = report_service.generate_container_report(
        container_id,
        data,
        logo,
        signature,
        from_date,
        to_date
    )

    file_path = result["file"]

    # -------- FORMAT FILE NAME --------
    date_str = datetime.now().strftime("%Y%m%d")
    download_name = f"container_{container_id}_{date_str}.pdf"

    # -------- CREATE RESPONSE --------
    response = FileResponse(
        path=file_path,
        filename=download_name,
        media_type="application/pdf"
    )

    # -------- ADD HEADER (PRO LEVEL) --------
    response.headers["Content-Disposition"] = f"attachment; filename={download_name}"

    # -------- AUTO DELETE FILE AFTER RESPONSE --------
    response.background = BackgroundTask(lambda: os.remove(file_path))

    return response


@router.post("/report/preview/{container_id}")
def preview_report(
    container_id: str,
    data: dict,
    from_date: str,
    to_date: str
):
    result = report_service.generate_container_report(
        container_id,
        data,
        None,   # ❗ no logo required for preview (or optional)
        None,
        from_date,
        to_date
    )

    return FileResponse(
        path=result["file"],
        media_type="application/pdf",
        filename="preview.pdf"
    )
    

'''
def get_template_environment():
    """
    Create and return Jinja2 template environment.
    """
    return Environment(
        loader=FileSystemLoader("app/templates")
    )

@router.get("/preview", response_class=HTMLResponse)
def preview_report():
    """
    Preview WHO GDP report in browser.
    """
    data = get_report_data()

    env = get_template_environment()
    template = env.get_template("who_gdp.html")

    html_content = template.render(**data)

    return html_content


@router.post("/generate")
def generate_report():
    """
    Generate WHO GDP report as PDF.
    """
    data = get_report_data()

    env = get_template_environment()
    template = env.get_template("who_gdp.html")

    html_content = template.render(**data)

    pdfkit.from_string(html_content, "report.pdf")

    return {"message": "PDF generated successfully"}'''