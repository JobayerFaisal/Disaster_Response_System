# placeholder
import json
from backend.agents.Others.base import llm, safe_json
from tools.weather_api import get_weather_forecast

SYSTEM_PROMPT = """
You are the Weather Intelligence Agent.
Input is RAW weather data from APIs.

Output must be valid JSON:
{
  "rainfall_mm": number,
  "alert_level": "GREEN|YELLOW|ORANGE|RED",
  "storm_probability": number,
  "summary": string
}
"""

def run(state):
    raw = get_weather_forecast()
    model = llm()

    prompt = f"{SYSTEM_PROMPT}\nRAW_DATA:\n{json.dumps(raw)}"

    resp = model.invoke(prompt).content
    state.weather = safe_json(resp)
    return state
