# placeholder
import json
from backend.agents.Others.base import llm_json

PROMPT = """
You are the Rescue Routing Agent.
Create safe rescue routes.
Output:
[
 {"team": "A1", "route": ["x1,y1","x2,y2"], "eta_min": 12 }
]
"""

def run(state):
    llm = llm_json()
    resp = llm.invoke(f"{PROMPT}\n{json.dumps(state.triaged_sos)}")
    state.routes = json.loads(resp.content)
    return state
