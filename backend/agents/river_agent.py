# placeholder
import json
from agents.base import llm_json

PROMPT = """
You are the River Monitoring Agent.
Input: Sensor readings (water level, rise rate, flow speed).
Output JSON:
{
 "water_level_m": float,
 "rise_rate_cm_hr": float,
 "overflow_risk": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
 "alert": "GREEN" | "YELLOW" | "ORANGE" | "RED"
}
"""

def run(state):
    raw = {
        "water_level": 6.2,
        "rise_rate": 14.4
    }

    llm = llm_json()
    resp = llm.invoke(f"{PROMPT}\n{json.dumps(raw)}")
    state.river = json.loads(resp.content)
    return state
