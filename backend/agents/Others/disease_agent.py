# placeholder
import json
from backend.agents.Others.base import llm_json

PROMPT = """
You are the Disease Risk Prediction Agent.
Predict disease outbreaks (cholera, diarrhea, dengue).
Output:
{
 "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
 "likely_diseases": [...],
 "recommendations": "..."
}
"""

def run(state):
    llm = llm_json()
    resp = llm.invoke(f"{PROMPT}\n{json.dumps(state.flood_map)}")
    state.disease_risk = json.loads(resp.content)
    return state
