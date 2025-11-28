# placeholder
import json
from backend.agents.Others.base import llm_json

PROMPT = """
You are the Emergency Hotline Agent.
Extract structured emergency calls.
Output:
[
 {"caller": "...", "message": "...", "people": 3, "severity": 0-100}
]
"""

def run(state):
    calls = [
        "We are trapped on the roof, water rising fast!",
        "Old man stuck in flooded house, needs evacuation."
    ]

    llm = llm_json()
    resp = llm.invoke(f"{PROMPT}\n{json.dumps(calls)}")
    state.hotline_sos = json.loads(resp.content)
    return state
