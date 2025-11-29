# backend/agents/manual_report_agent/agent.py

from backend.agents.manual_report_agent.db import get_connection
from backend.agents.manual_report_agent.report_model import Report
from datetime import datetime

def save_report(report: Report):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        INSERT INTO manual_reports (user_id, location, severity, description, timestamp)
        VALUES (%s, %s, %s, %s, %s)
    """
    
    cursor.execute(query, (report.user_id, report.location, report.severity, report.description, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Report from {report.user_id} saved successfully!")

def submit_report(user_id, location, severity, description):
    new_report = Report(user_id, location, severity, description)
    save_report(new_report)
