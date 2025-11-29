import streamlit as st
from dashboard.db import query
import plotly.express as px

import sys
import os

# Add the root project directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


st.title("🌧 Real-Time Weather Data")

df = query("""
    SELECT 
        zone_id,
        timestamp,
        temperature,
        humidity,
        pressure,
        wind_speed,
        precipitation_1h,
        condition
    FROM weather_data
    ORDER BY timestamp DESC
    LIMIT 200
""")

st.dataframe(df)

fig = px.line(
    df.sort_values("timestamp"),
    x="timestamp", y="temperature",
    title="🌡 Temperature Trend"
)
st.plotly_chart(fig, use_container_width=True)
