# placeholder
import json
from agents.base import llm_json

PROMPT = """
You are the Flood Simulation Agent.
Use weather + river to predict flood spread.
Output:
{
 "zones": [
    {"area": "north", "risk": "RED", "depth_m": 1.2},
    {"area": "south", "risk": "YELLOW", "depth_m": 0.5}
 ],
 "geojson": {...}
}
"""

def run(state):
    llm = llm_json()
    input_data = {
        "weather": state.weather,
        "river": state.river
    }

    resp = llm.invoke(f"{PROMPT}\n{json.dumps(input_data)}")
    state.flood_map = json.loads(resp.content)
    return state
