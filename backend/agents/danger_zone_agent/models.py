from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel
from typing import List, Optional

from backend.agents.environmental_agent.models import (
    SentinelZone, GeoPoint, SeverityLevel
)


class DangerZoneReport(BaseModel):
    id: UUID = uuid4()
    zone: SentinelZone
    timestamp: datetime = datetime.utcnow()
    affected_area_km2: float
    severity: SeverityLevel
    cluster_count: int
    nearby_reports: int
    risk_score: float
    critical_infrastructure: List[str]
    recommended_actions: List[str]
