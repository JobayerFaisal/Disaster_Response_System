# placeholder
import json
from backend.agents.Others.base import llm_json

PROMPT = """
You are the Drone Vision Agent.
You analyze drone observations for:
- submerged houses
- blocked bridges
- stranded people

Output JSON:
{
  "damaged_bridges": int,
  "people_detected": int,
  "blocked_roads": int,
  "critical_observation": "..."
}
"""

def run(state):
    mock_input = {
        "drone": "bridge half-submerged, 12 people waving on rooftop"
    }

    llm = llm_json()
    resp = llm.invoke(f"{PROMPT}\n{json.dumps(mock_input)}")
    state.drone_analysis = json.loads(resp.content)
    return state
