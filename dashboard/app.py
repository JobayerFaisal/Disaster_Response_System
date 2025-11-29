import streamlit as st

st.set_page_config(
    page_title="AI Disaster Intelligence Dashboard",
    page_icon="🌎",
    layout="wide"
)

st.title("🌎 AI Disaster Intelligence — Control Center")
st.caption("Real-time environmental intelligence powered by multi-agent AI")

st.write("Use the navigation menu to explore:")
st.markdown("""
- 🌧 **Real-Time Weather Data**  
- 🔮 **AI Predictions**  
- ⚠️ **Danger Zone Analysis**  
- 🛰 **Map Visualization**  
- 🧠 **Agent Logs**  
""")
