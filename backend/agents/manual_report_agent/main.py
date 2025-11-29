# backend/agents/manual_report_agent/main.py

from backend.agents.manual_report_agent.agent import submit_report
from backend.agents.manual_report_agent.db import create_reports_table

# Initialize the database (only once)
create_reports_table()

# Example usage: Submit a new manual report
submit_report(1, "Dhaka", "High", "Severe flooding after heavy rains.")
