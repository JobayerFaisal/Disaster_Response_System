# placeholder
import json
from agents.base import llm_json

PROMPT = """
You are the Resource Allocation Agent.
Decide where to send:
- boats
- food
- medical units

Output:
{
 "boats": [...],
 "medical": [...],
 "supplies": [...]
}
"""

def run(state):
    llm = llm_json()
    resp = llm.invoke(f"{PROMPT}\n{json.dumps(state.infrastructure)}")
    state.resource_plan = json.loads(resp.content)
    return state
