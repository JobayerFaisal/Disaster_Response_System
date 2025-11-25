from core.db import SessionLocal
from core.models import SimulationDay

def save_simulation_day(state):
    db = SessionLocal()

    obj = SimulationDay(
        day=state.day,
        weather=state.weather,
        river=state.river,
        flood_map=state.flood_map,
        drone_analysis=state.drone_analysis,
        infrastructure=state.infrastructure,
        social_media_sos=state.social_media_sos,
        hotline_sos=state.hotline_sos,
        triaged_sos=state.triaged_sos,
        routes=state.routes,
        resource_plan=state.resource_plan,
        disease_risk=state.disease_risk,
        coordinator=state.coordinator,
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)
    db.close()

    return obj.id
