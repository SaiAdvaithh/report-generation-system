from fastapi import UploadFile, File, Form
from app.models.report_request import ReportRequest

@router.post("/report/{container_id}")
async def generate_report(
    container_id: str,
    company_name: str = Form(...),
    facility_name: str = Form(...),
    address: str = Form(...),
    report_id: str = Form(...),
    auditor: str = Form(...),
    reviewer: str = Form(...),
    approver: str = Form(...),
    logo: UploadFile = File(...),
    signature: UploadFile = File(...)
):

    report = report_service.generate_container_report(
        container_id,
        {
            "company_name": company_name,
            "facility_name": facility_name,
            "address": address,
            "report_id": report_id,
            "auditor": auditor,
            "reviewer": reviewer,
            "approver": approver
        },
        logo,
        signature
    )

    return report