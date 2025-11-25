# placeholder
import json
from agents.base import llm_json

PROMPT = """
You are the Coordinator Agent.
You read all other agents’ outputs and produce a final decision.
Output:
{
 "summary": "...",
 "critical_actions": [...],
 "warnings": [...],
 "next_steps": [...]
}
"""

def run(state):
    llm = llm_json()

    data = {
        "weather": state.weather,
        "river": state.river,
        "flood_map": state.flood_map,
        "drone": state.drone_analysis,
        "infra": state.infrastructure,
        "sos": state.triaged_sos,
        "routes": state.routes,
        "resources": state.resource_plan,
        "disease": state.disease_risk
    }

    resp = llm.invoke(f"{PROMPT}\n{json.dumps(data)}")
    state.coordinator = json.loads(resp.content)
    return state
