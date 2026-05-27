from pydantic import BaseModel

class ReportRequest(BaseModel):
    company_name: str
    facility_name: str
    address: str
    report_id: str
    auditor: str
    reviewer: str
    approver: str