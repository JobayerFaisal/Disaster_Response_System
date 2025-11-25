# placeholder
from pydantic import BaseModel
from typing import Optional, Dict, List, Any

class FloodState(BaseModel):
    day: int = 0

    weather: Optional[Dict[str, Any]] = None
    river: Optional[Dict[str, Any]] = None
    flood_map: Optional[Dict[str, Any]] = None
    drone_analysis: Optional[Dict[str, Any]] = None
    infrastructure: Optional[Dict[str, Any]] = None

    social_media_sos: Optional[List[dict]] = None
    hotline_sos: Optional[List[dict]] = None
    triaged_sos: Optional[List[dict]] = None

    routes: Optional[List[dict]] = None
    resource_plan: Optional[Dict[str, Any]] = None
    disease_risk: Optional[Dict[str, Any]] = None

    coordinator: Optional[Dict[str, Any]] = None
