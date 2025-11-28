# placeholder
import json
from backend.agents.Others.base import llm_json

PROMPT = """
You are the Infrastructure Assessment Agent.
Analyze:
- hospitals
- power grid
- shelters
- road conditions

Output:
{
 "hospitals": {"capacity": "...", "status": "..."},
 "roads": [{"name": "...", "status": "OPEN|CLOSED"}],
 "power_grid": "...",
 "shelter_updates": [...]
}
"""

def run(state):
    input_data = {
        "drone": state.drone_analysis,
        "flood": state.flood_map
    }

    llm = llm_json()
    resp = llm.invoke(f"{PROMPT}\n{json.dumps(input_data)}")
    state.infrastructure = json.loads(resp.content)
    return state
