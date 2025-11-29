import streamlit as st
from dashboard.db import query
import plotly.express as px

st.title("🔮 AI Flood Predictions")

df = query("""
    SELECT zone_id, timestamp, risk_score, severity_level, confidence
    FROM flood_predictions
    ORDER BY timestamp DESC
    LIMIT 200
""")

st.dataframe(df)

fig = px.line(
    df.sort_values("timestamp"),
    x="timestamp", y="risk_score",
    title="📈 Flood Risk Score Trend"
)
st.plotly_chart(fig, use_container_width=True)
