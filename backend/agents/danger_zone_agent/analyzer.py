from typing import List
from uuid import uuid4
from datetime import datetime

from backend.agents.environmental_agent.spatial_analyzer import (
    PostGISSpatialAnalyzer
)
from backend.agents.environmental_agent.models import SeverityLevel
from backend.agents.danger_zone_agent.models import DangerZoneReport


class DangerZoneAnalyzer:

    def __init__(self, spatial: PostGISSpatialAnalyzer):
        self.spatial = spatial

    async def analyze_zone(self, zone):
        """Perform all spatial checks for a zone."""

        # Nearby flood reports
        reports = await self.spatial.find_nearby_flood_reports(
            center=zone.center,
            radius_km=zone.radius_km,
            since_hours=24
        )

        nearby_reports = len(reports)

        # Compute affected area
        affected_area = await self.spatial.calculate_affected_area(zone)

        # Find risk clusters
        clusters = await self.spatial.find_risk_clusters(zone)
        cluster_count = len(clusters) if clusters else 0

        # Compute severity level
        if cluster_count >= 3 or affected_area > 2:
            severity = SeverityLevel.HIGH
        elif cluster_count >= 1 or affected_area > 0.5:
            severity = SeverityLevel.MODERATE
        elif nearby_reports > 0:
            severity = SeverityLevel.LOW
        else:
            severity = SeverityLevel.MINIMAL

        # Basic risk scoring
        risk_score = min(
            (affected_area / 5) +
            (cluster_count * 0.2) +
            (nearby_reports * 0.05),
            1.0
        )

        # Infrastructure at risk 
        infra = await self.spatial._identify_critical_infrastructure(zone, affected_area)

        # Suggested actions
        actions = []
        if severity == SeverityLevel.HIGH:
            actions.append("Issue urgent flood warning.")
            actions.append("Prepare evacuation routes.")
        elif severity == SeverityLevel.MODERATE:
            actions.append("Increase monitoring frequency.")
        elif severity == SeverityLevel.LOW:
            actions.append("Maintain observation.")

        return DangerZoneReport(
            id=uuid4(),
            zone=zone,
            timestamp=datetime.utcnow(),
            affected_area_km2=affected_area,
            severity=severity,
            cluster_count=cluster_count,
            nearby_reports=nearby_reports,
            risk_score=risk_score,
            critical_infrastructure=infra,
            recommended_actions=actions
        )
