# backend/agents/manual_report_agent/run.py

def run(user_id, location, severity, description):
    """
    Process and save a manual report. This function should handle the
    report data and store it in the database, or process it as needed.
    """
    # Here you can process the report (e.g., save it to the database)
    # Example of logging or saving the report (you should implement actual storage logic)
    print(f"Processing report from User {user_id}: {location}, {severity}, {description}")

    # Implement the saving or further processing logic here
    # For example, saving the report to a database or running some analysis

    return {"status": "success", "message": "Report processed successfully"}
