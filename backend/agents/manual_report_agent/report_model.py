# backend/agents/manual_report_agent/report_model.py

class Report:
    def __init__(self, user_id, location, severity, description):
        self.user_id = user_id
        self.location = location
        self.severity = severity
        self.description = description
