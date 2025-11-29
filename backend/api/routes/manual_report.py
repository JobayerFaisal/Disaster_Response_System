from fastapi import APIRouter
from backend.agents.manual_report_agent.run import run as run_manual_report
from pydantic import BaseModel

# Initialize the router
router = APIRouter()

# Define the structure of the report submission payload using Pydantic
class ReportSubmission(BaseModel):
    user_id: int
    location: str
    severity: str
    description: str

@router.post("/submit_report")
async def submit_report(report: ReportSubmission):
    """Submit a manual report."""
    try:
        # Pass the report to your manual report agent
        result = run_manual_report(report.user_id, report.location, report.severity, report.description)
        return {"status": "success", "message": "Report submitted successfully", "data": result}
    except Exception as e:
        return {"status": "failed", "message": str(e)}
