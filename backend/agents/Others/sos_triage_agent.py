# placeholder
import json
from agents.base import llm_json

PROMPT = """
You are the SOS Triage Agent.
You merge hotline + social media → prioritize.
Output:
[
 {"source": "hotline|social", "location": "...", "priority": "LOW|MEDIUM|HIGH|CRITICAL"}
]
"""

def run(state):
    data = {
        "social": state.social_media_sos,
        "hotline": state.hotline_sos
    }

    llm = llm_json()
    resp = llm.invoke(f"{PROMPT}\n{json.dumps(data)}")
    state.triaged_sos = json.loads(resp.content)
    return state
