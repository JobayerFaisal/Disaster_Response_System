import streamlit as st
from dashboard.db import query
import plotly.express as px

st.title("⚠️ Danger Zone Analysis")

df = query("""
    SELECT 
        zone_id,
        timestamp,
        affected_area_km2,
        severity_level,
        cluster_count,
        nearby_reports,
        risk_score
    FROM danger_zone_reports
    ORDER BY timestamp DESC
    LIMIT 200
""")

st.dataframe(df)

fig = px.scatter(
    df,
    x="timestamp",
    y="risk_score",
    color="severity_level",
    size="affected_area_km2",
    title="⚠️ Danger Zone Risk Over Time"
)

st.plotly_chart(fig, use_container_width=True)
