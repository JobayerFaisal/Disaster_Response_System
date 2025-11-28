import asyncio
import os
import json
import asyncpg
from dotenv import load_dotenv

from backend.agents.environmental_agent.data_collectors import (
    WeatherAPICollector,
    DataCollectionOrchestrator
)

from backend.agents.environmental_agent.data_processors import (
    LLMEnrichmentProcessor,
    WeatherDataNormalizer,
    SocialMediaAnalyzer,
    DataProcessingOrchestrator
)

from backend.agents.environmental_agent.predictor import (
    FloodRiskPredictor,
    AlertGenerator,
    PredictionOrchestrator
)

from backend.agents.environmental_agent.spatial_analyzer import (
    PostGISSpatialAnalyzer
)

from backend.agents.environmental_agent.models import (
    SentinelZone,
    GeoPoint,
    SeverityLevel
)

load_dotenv()



async def main():
    print("🚀 Starting Environmental Intelligence Agent (Weather + OpenAI + PostgreSQL)...")

    # ----------------------------------------------------------------------
    # 1. Load environment variables
    # ----------------------------------------------------------------------
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    WEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")

    if not OPENAI_API_KEY:
        raise ValueError("❌ OPENAI_API_KEY missing in .env")

    if not WEATHER_KEY:
        raise ValueError("❌ OPENWEATHER_API_KEY missing in .env")

    DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    # ----------------------------------------------------------------------
    # 2. Create PostgreSQL connection pool
    # ----------------------------------------------------------------------
    print("🔗 Connecting to PostgreSQL...")
    pool = await asyncpg.create_pool(DATABASE_URL)
    assert pool is not None, "Database connection failed."

    # ----------------------------------------------------------------------
    # 3. Initialize Spatial Analyzer (creates tables)
    # ----------------------------------------------------------------------
    spatial_analyzer = PostGISSpatialAnalyzer(pool)
    await spatial_analyzer.initialize_schema()

    # Create alerts table (not part of initialize_schema)
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS environmental_alerts (
                id UUID PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL,
                alert_type VARCHAR(50) NOT NULL,
                severity VARCHAR(50) NOT NULL,
                zone_id UUID REFERENCES sentinel_zones(id),
                prediction_id UUID REFERENCES flood_predictions(id),
                message TEXT NOT NULL,
                priority INT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """)

    # ----------------------------------------------------------------------
    # 4. Initialize Weather Collector only (no Twitter)
    # ----------------------------------------------------------------------
    weather_collector = WeatherAPICollector(api_key=WEATHER_KEY, cache_client=None)
    collector_orchestrator = DataCollectionOrchestrator(
        weather_collector=weather_collector,
        social_collector=None
    )

    # ----------------------------------------------------------------------
    # 5. Initialize Processing Pipeline
    # ----------------------------------------------------------------------
    llm_processor = LLMEnrichmentProcessor(api_key=OPENAI_API_KEY)
    weather_normalizer = WeatherDataNormalizer()
    social_analyzer = SocialMediaAnalyzer()  # must stay for orchestrator

    processor_orchestrator = DataProcessingOrchestrator(
        llm_processor=llm_processor,
        weather_normalizer=weather_normalizer,
        social_analyzer=social_analyzer
    )

    # ----------------------------------------------------------------------
    # 6. Initialize Predictor
    # ----------------------------------------------------------------------
    predictor = FloodRiskPredictor()
    alert_generator = AlertGenerator()
    prediction_orchestrator = PredictionOrchestrator(
        predictor=predictor,
        alert_generator=alert_generator
    )

    # ----------------------------------------------------------------------
    # 7. Define Monitoring Zones
    # ----------------------------------------------------------------------
    zones = [
        SentinelZone(
            name="Dhaka Center",
            center=GeoPoint(latitude=23.8103, longitude=90.4125),
            radius_km=5,
            risk_level=SeverityLevel.MODERATE,
            population_density=None,
            elevation=None,
            drainage_capacity=None
        )
    ]

    # Save zones in DB
    for z in zones:
        await spatial_analyzer.store_sentinel_zone(z)

    # ----------------------------------------------------------------------
    # 8. Collect Weather Data
    # ----------------------------------------------------------------------
    print("🌧️ Collecting weather data...")
    collected_data = await collector_orchestrator.collect_all_zones(zones)

    # Save raw weather to DB
    for item in collected_data:
        weather = item["weather"]
        zone = item["zone"]

        if weather:
            await spatial_analyzer.store_weather_data(weather, zone_id=str(zone.id))

    # ----------------------------------------------------------------------
    # 9. Process Data (Weather-only)
    # ----------------------------------------------------------------------
    print("⚙️ Processing weather data...")
    processed_data = await processor_orchestrator.process_all_zones(collected_data)

    # ----------------------------------------------------------------------
    # 10. Predictions + Alerts
    # ----------------------------------------------------------------------
    print("🔮 Generating predictions...")
    predictions, alerts = await prediction_orchestrator.predict_all_zones(processed_data)

    # ----------------------------------------------------------------------
    # 11. Save Predictions
    # ----------------------------------------------------------------------
    async with pool.acquire() as conn:
        for pred in predictions:
            await conn.execute(
                """
                INSERT INTO flood_predictions (
                    id, zone_id, timestamp, risk_score, severity_level,
                    confidence, time_to_impact_hours, affected_area_km2,
                    risk_factors, recommended_actions
                ) VALUES (
                    $1, $2, $3, $4, $5,
                    $6, $7, $8,
                    $9, $10
                )
                """,
                pred.id,
                pred.zone.id,
                pred.timestamp,
                pred.risk_score,
                pred.severity_level.value,
                pred.confidence,
                pred.time_to_impact_hours,
                pred.affected_area_km2,
                json.dumps(pred.risk_factors.model_dump()),  # FIXED
                json.dumps(pred.recommended_actions)          # FIXED
            )

    # ----------------------------------------------------------------------
    # 12. Save Alerts
    # ----------------------------------------------------------------------
    async with pool.acquire() as conn:
        for alert in alerts:
            await conn.execute(
                """
                INSERT INTO environmental_alerts (
                    id, timestamp, alert_type, severity, zone_id,
                    prediction_id, message, priority
                ) VALUES (
                    $1, $2, $3, $4, $5,
                    $6, $7, $8
                )
                """,
                alert.id,
                alert.timestamp,
                alert.alert_type.value,
                alert.severity.value,
                alert.zone.id,
                alert.prediction.id,
                alert.message,
                alert.priority
            )

    # ----------------------------------------------------------------------
    # 13. Output Results
    # ----------------------------------------------------------------------
    print("\n================== RESULTS ==================")
    for pred in predictions:
        print(f"Zone: {pred.zone.name}")
        print(f"Risk Score: {pred.risk_score:.2f}")
        print(f"Severity: {pred.severity_level.value}")
        print(f"Confidence: {pred.confidence:.2f}")
        print("------------------------------------------------")

    print("\n=============== ALERTS ==================")
    for alert in alerts:
        print(alert.message)
        print("--------------------------------------------")

    print("\n🎉 Agent run completed! (Weather-only + DB Saved)")



def run():
    # import asyncio
    return asyncio.run(main())


# if __name__ == "__main__":
#     asyncio.run(main())
