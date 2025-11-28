# placeholder
from langgraph.graph import StateGraph, END
from graph.state import FloodState
from graph.timeline import advance_day

from agents.weather_agent import run as weather_agent
from backend.agents.Others.river_agent import run as river_agent
from agents.flood_sim_agent import run as flood_agent
from agents.image_agent import run as image_agent
from agents.infrastructure_agent import run as infra_agent
from agents.social_media_agent import run as social_agent
from agents.hotline_agent import run as hotline_agent
from agents.sos_triage_agent import run as triage_agent
from agents.routing_agent import run as routing_agent
from agents.resource_agent import run as resource_agent
from backend.agents.Others.disease_agent import run as disease_agent
from backend.agents.Others.coordinator_agent import run as coordinator_agent

def build_workflow():
    g = StateGraph(FloodState)

    g.set_entry_point("weather")
    g.add_node("weather", weather_agent)
    g.add_edge("weather", "river")

    g.add_node("river", river_agent)
    g.add_edge("river", "flood")

    g.add_node("flood", flood_agent)
    g.add_edge("flood", "advance")

    g.add_node("advance", advance_day)
    g.add_edge("advance", "image")

    g.add_node("image", image_agent)
    g.add_edge("image", "infra")

    g.add_node("infra", infra_agent)
    g.add_edge("infra", "social")

    g.add_node("social", social_agent)
    g.add_edge("social", "hotline")

    g.add_node("hotline", hotline_agent)
    g.add_edge("hotline", "advance")

    g.add_edge("advance", "triage")
    g.add_node("triage", triage_agent)
    g.add_edge("triage", "routing")

    g.add_node("routing", routing_agent)
    g.add_edge("routing", "resource")

    g.add_node("resource", resource_agent)
    g.add_edge("resource", "advance")

    g.add_node("disease", disease_agent)
    g.add_edge("advance", "disease")

    g.add_node("coordinator", coordinator_agent)

    def loop(state):
        return END if state.day >= 7 else "coordinator"

    g.add_conditional_edges("disease", loop)

    return g.compile()

app = build_workflow()
