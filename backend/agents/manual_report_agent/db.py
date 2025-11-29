# backend/agents/manual_report_agent/db.py

import psycopg2
from backend.agents.manual_report_agent.config import Config

def get_connection():
    return psycopg2.connect(
        host=Config.POSTGRES_HOST,
        database=Config.POSTGRES_DB,
        user=Config.POSTGRES_USER,
        password=Config.POSTGRES_PASSWORD,
        port=Config.POSTGRES_PORT
    )

def create_reports_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS manual_reports (
            id SERIAL PRIMARY KEY,
            user_id INT,
            location VARCHAR(255),
            severity VARCHAR(50),
            description TEXT,
            timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()
