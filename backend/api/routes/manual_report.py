from fastapi import APIRouter
from backend.agents.manual_report_agent.run import run as run_manual_report
from pydantic import BaseModel
import logging

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
        # Log incoming data for debugging
        logging.info(f"Received report: {report.dict()}")
        
        # Pass the report to your manual report agent
        result = run_manual_report(report.user_id, report.location, report.severity, report.description)

        if result["status"] == "success":
            return {"status": "success", "message": "Report submitted successfully", "data": result}
        else:
            logging.error(f"Manual report submission failed: {result['message']}")
            return {"status": "failed", "message": "Failed to submit the report."}
    except Exception as e:
        # Log the error for better debugging
        logging.error(f"Error submitting report: {str(e)}")
        return {"status": "failed", "message": f"Error submitting the report: {str(e)}"}
