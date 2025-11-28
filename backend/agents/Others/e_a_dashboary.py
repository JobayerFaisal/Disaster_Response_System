import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# --------------------------------
# Load environment variables
# --------------------------------
load_dotenv()

# --------------------------------
# Create SQLAlchemy Engine
# --------------------------------
def get_engine():
    db_url = (
        f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    )
    return create_engine(db_url)


# --------------------------------
# Load table helper
# --------------------------------
def load_table(table_name, order_by="timestamp"):
    engine = get_engine()
    return pd.read_sql(f"SELECT * FROM {table_name} ORDER BY {order_by} DESC", engine)


# --------------------------------
# Streamlit Page Config
# --------------------------------
st.set_page_config(
    page_title="Disaster AI Dashboard",
    page_icon="🌧",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .main {
            background-color: #0d1117;
            color: white;
        }
        .stDataFrame {
            background-color: #161b22;
        }
        .stAlert {
            border-radius: 8px;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🌧 Disaster AI — Environmental Intelligence Dashboard")

# Auto-refresh every X seconds (optional)
refresh = st.sidebar.slider("Auto-refresh interval (seconds)", 0, 60, 0)
if refresh > 0:
    st.experimental_set_query_params(refresh=str(refresh))
    st.rerun()


# =====================================================
# TABS
# =====================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📍 Zones",
    "🌦 Weather Data",
    "🔮 Predictions",
    "🚨 Alerts",
])


# =====================================================
# TAB 1 — ZONES
# =====================================================
with tab1:
    st.header("📍 Monitored Zones")

    engine = get_engine()
    zones_df = pd.read_sql("SELECT * FROM sentinel_zones ORDER BY created_at DESC", engine)

    st.dataframe(
        zones_df,
        use_container_width=True,
        height=400
    )

    if not zones_df.empty:
        st.subheader("🗺 Zone Locations")
        fig = px.scatter_mapbox(
            zones_df,
            lat="center_lat",
            lon="center_lon",
            zoom=4,
            color="id",
            height=500
        )
        fig.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig, use_container_width=True)


# =====================================================
# TAB 2 — WEATHER DATA
# =====================================================
with tab2:
    st.header("🌦 Latest Weather Observations")

    weather_df = load_table("weather_data")
    st.dataframe(weather_df, use_container_width=True)

    if not weather_df.empty:
        col1, col2 = st.columns(2)

        with col1:
            fig = px.line(
                weather_df.sort_values("timestamp"),
                x="timestamp",
                y="temperature",
                title="🌡 Temperature Trend",
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.line(
                weather_df.sort_values("timestamp"),
                x="timestamp",
                y="rain_1h",
                title="🌧 Rainfall (1h) Trend",
            )
            st.plotly_chart(fig, use_container_width=True)


# =====================================================
# TAB 3 — PREDICTIONS
# =====================================================
with tab3:
    st.header("🔮 Flood Risk Predictions")

    predictions_df = load_table("flood_predictions", order_by="created_at")
    st.dataframe(predictions_df, use_container_width=True)

    if not predictions_df.empty:
        col1, col2 = st.columns(2)

        with col1:
            fig = px.line(
                predictions_df,
                x="timestamp",
                y="risk_score",
                title="📈 Flood Risk Over Time",
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.bar(
                predictions_df,
                x="timestamp",
                y="severity_level",
                title="🟥 Severity Levels Over Time",
                color="severity_level"
            )
            st.plotly_chart(fig, use_container_width=True)


# =====================================================
# TAB 4 — ALERTS
# =====================================================
with tab4:
    st.header("🚨 Emergency Alerts")

    alerts_df = load_table("environmental_alerts")
    st.dataframe(alerts_df, use_container_width=True)

    if not alerts_df.empty:
        st.subheader("🔥 Latest Alert")
        latest = alerts_df.iloc[0]

        severity_color = {
            "LOW": "green",
            "MEDIUM": "orange",
            "HIGH": "red",
            "CRITICAL": "darkred"
        }.get(latest["severity"].upper(), "blue")

        st.markdown(f"""
        <div style="
            background-color: {severity_color}; 
            padding: 12px; 
            border-radius: 10px;
            color: white;
            font-size: 18px;
            margin-bottom: 15px;
        ">
        <b>Zone:</b> {latest['zone_id']}<br>
        <b>Severity:</b> {latest['severity']}<br>
        <b>Alert Type:</b> {latest['alert_type']}<br>
        <b>Message:</b> {latest['message']}<br>
        <b>Priority:</b> {latest['priority']}<br>
        </div>
        """, unsafe_allow_html=True)
