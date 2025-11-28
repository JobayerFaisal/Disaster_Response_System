# placeholder
import json
from backend.agents.Others.base import llm_json

PROMPT = """
You are the Social Media SOS Agent.
Extract urgent SOS posts.
Output:
[
 {"text": "...", "location": "...", "urgency": 0-100},
 ...
]
"""

def run(state):
    raw_posts = [
        "Water entering my house, we're stuck at 2nd floor!",
        "Need urgent help in South District!"
    ]

    llm = llm_json()
    resp = llm.invoke(f"{PROMPT}\n{json.dumps(raw_posts)}")
    state.social_media_sos = json.loads(resp.content)
    return state
