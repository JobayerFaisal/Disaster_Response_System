import asyncio
import asyncpg
import os
import json
from dotenv import load_dotenv

from backend.agents.danger_zone_agent.analyzer import DangerZoneAnalyzer
from backend.agents.environmental_agent.spatial_analyzer import PostGISSpatialAnalyzer
from backend.agents.environmental_agent.models import SentinelZone, GeoPoint, SeverityLevel

load_dotenv()

async def main():
    print("🛰️ Running Danger Zone Agent...")

    # Load DB settings
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")

    DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    print("🔗 Connecting to PostgreSQL...")
    pool = await asyncpg.create_pool(DATABASE_URL)

    spatial = PostGISSpatialAnalyzer(pool)
    analyzer = DangerZoneAnalyzer(spatial)


    spatial = PostGISSpatialAnalyzer(pool)
    analyzer = DangerZoneAnalyzer(spatial)

    # Load all zones
    async with pool.acquire() as p:
        rows = await p.fetch("SELECT id, name FROM sentinel_zones;")

    reports = []

    for row in rows:
        zone_id = row["id"]
        zone = await spatial.db_pool.fetchrow("""
            SELECT 
                name,
                radius_km,
                population_density,
                elevation,
                drainage_capacity,
                risk_level,
                ST_X(center::geometry) as lon,
                ST_Y(center::geometry) as lat
            FROM sentinel_zones 
            WHERE id=$1
        """, zone_id)

        z = SentinelZone(
            id=zone_id,
            name=zone["name"],
            radius_km=zone["radius_km"],
            center=GeoPoint(latitude=zone["lat"], longitude=zone["lon"]),
            risk_level=SeverityLevel(zone["risk_level"]) if zone["risk_level"] else SeverityLevel.MINIMAL,
            population_density=zone["population_density"],
            elevation=zone["elevation"],
            drainage_capacity=zone["drainage_capacity"]
        )



        report = await analyzer.analyze_zone(z)
        reports.append(report)

        # Save report
        async with pool.acquire() as c:
            await c.execute("""
                INSERT INTO danger_zone_reports (
                    id, zone_id, timestamp, affected_area_km2, severity_level,
                    cluster_count, nearby_reports, risk_score,
                    critical_infrastructure, recommended_actions
                ) VALUES (
                    $1, $2, $3, $4, $5,
                    $6, $7, $8, $9, $10
                )
            """,
                report.id,
                report.zone.id,
                report.timestamp,
                report.affected_area_km2,
                report.severity.value,
                report.cluster_count,
                report.nearby_reports,
                report.risk_score,
                json.dumps(report.critical_infrastructure),  # ✔ JSONB
                json.dumps(report.recommended_actions)       # ✔ JSONB
            )

    print("🛰️ Done. Danger zone analysis complete.")
    return reports


# Sync wrapper
def run():
    return asyncio.run(main())

