import streamlit as st
from dashboard.db import query

st.title("🧠 Agent Logs")

df = query("""
    SELECT * FROM agent_logs
    ORDER BY timestamp DESC
    LIMIT 200
""")

st.dataframe(df)
