import asyncio
import os
import json
import asyncpg
from dotenv import load_dotenv

from backend.agents.environmental_agent.data_collectors import (
    WeatherAPICollector,
    DataCollectionOrchestrator,
)

from backend.agents.environmental_agent.data_processors import (
    LLMEnrichmentProcessor,
    WeatherDataNormalizer,
    SocialMediaAnalyzer,
    DataProcessingOrchestrator,
)

from backend.agents.environmental_agent.predictor import (
    FloodRiskPredictor,
    AlertGenerator,
    PredictionOrchestrator,
)

from backend.agents.environmental_agent.spatial_analyzer import (
    PostGISSpatialAnalyzer,
)
        

        

from backend.agents.environmental_agent.models import (
    SentinelZone,
    GeoPoint,
    SeverityLevel,
)

load_dotenv()


def _obj_to_dict(o):
    """
    Best-effort conversion of pydantic / dataclass / plain objects to dict
    so we can pretty-print them in the terminal.
    """
    if o is None:
        return None

    # Pydantic v2
    if hasattr(o, "model_dump"):
        try:
            return o.model_dump()
        except TypeError:
            return o.model_dump  # just in case it's a property

    # Pydantic v1
    if hasattr(o, "dict"):
        try:
            return o.dict()
        except TypeError:
            return o.dict  # just in case

    # Dataclass / normal object
    if hasattr(o, "__dict__"):
        return dict(o.__dict__)

    return str(o)


async def main():
    print("🚀 Starting Environmental Intelligence Agent (Weather + OpenAI + PostgreSQL)...")

    # ------------------------------------------------------------------
    # 1. Load environment variables
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # 2. Create PostgreSQL connection pool
    # ------------------------------------------------------------------
    print("🔗 Connecting to PostgreSQL...")
    pool = await asyncpg.create_pool(DATABASE_URL)
    assert pool is not None, "Database connection failed."

    try:
        # --------------------------------------------------------------
        # 3. Initialize Spatial Analyzer (creates tables)
        # --------------------------------------------------------------
        spatial_analyzer = PostGISSpatialAnalyzer(pool)
        await spatial_analyzer.initialize_schema()

        # Create alerts table (if not already created)
        async with pool.acquire() as conn:
            await conn.execute(
                """
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
                """
            )

        # --------------------------------------------------------------
        # 4. Initialize Weather Collector only (no Twitter)
        # --------------------------------------------------------------
        weather_collector = WeatherAPICollector(api_key=WEATHER_KEY, cache_client=None)
        collector_orchestrator = DataCollectionOrchestrator(
            weather_collector=weather_collector,
            social_collector=None,
        )

        # --------------------------------------------------------------
        # 5. Initialize Processing Pipeline
        # --------------------------------------------------------------
        llm_processor = LLMEnrichmentProcessor(api_key=OPENAI_API_KEY)
        weather_normalizer = WeatherDataNormalizer()
        social_analyzer = SocialMediaAnalyzer()  # kept for orchestrator compatibility

        processor_orchestrator = DataProcessingOrchestrator(
            llm_processor=llm_processor,
            weather_normalizer=weather_normalizer,
            social_analyzer=social_analyzer,
        )

        # --------------------------------------------------------------
        # 6. Initialize Predictor
        # --------------------------------------------------------------
        predictor = FloodRiskPredictor()
        alert_generator = AlertGenerator()
        prediction_orchestrator = PredictionOrchestrator(
            predictor=predictor,
            alert_generator=alert_generator,
        )

        # --------------------------------------------------------------
        # 7. Define Monitoring Zones (created once)
        # --------------------------------------------------------------
        zones = [
            SentinelZone(
                name="Sunamganj",
                center=GeoPoint(latitude=25.0658, longitude=91.3950),
                radius_km=5,
                risk_level=SeverityLevel.MODERATE,
                population_density=None,
                elevation=None,
                drainage_capacity=None,
            )
        ]


        # Save zones in DB (once)
        for z in zones:
            await spatial_analyzer.store_sentinel_zone(z)

        print("✅ Setup complete. Starting continuous monitoring loop...")
        print("   Press Ctrl+C in the terminal to stop.\n")

        # --------------------------------------------------------------
        # 8. Continuous loop: collect + process + predict every 30 sec
        # --------------------------------------------------------------
        cycle = 0
        while True:
            cycle += 1
            print(f"\n=================== CYCLE {cycle} ===================")

            # ----------------------------------------------------------
            # 8.1 Collect Weather Data
            # ----------------------------------------------------------
            print("🌧️ Collecting weather data...")
            collected_data = await collector_orchestrator.collect_all_zones(zones)

            # Show raw collected data in terminal
            print("\n📥 RAW COLLECTED DATA (weather per zone)")
            for item in collected_data:
                zone = item.get("zone")
                weather = item.get("weather")
                print("--------------------------------------------")
                print(f"Zone: {getattr(zone, 'name', 'Unknown')}")
                if weather:
                    weather_dict = _obj_to_dict(weather)
                    try:
                        pretty = json.dumps(weather_dict, indent=2, default=str)
                    except TypeError:
                        pretty = str(weather_dict)
                    print(pretty)
                else:
                    print("No weather data returned for this zone.")

            # Save raw weather to DB
            for item in collected_data:
                weather = item["weather"]
                zone = item["zone"]
                if weather:
                    await spatial_analyzer.store_weather_data(weather, zone_id=str(zone.id))

            # ----------------------------------------------------------
            # 8.2 Process Data
            # ----------------------------------------------------------
            print("\n⚙️ Processing weather data...")
            processed_data = await processor_orchestrator.process_all_zones(collected_data)

            # Show processed/normalized data
            print("\n🧮 PROCESSED / ENRICHED DATA")
            for p in processed_data:
                zone = p.get("zone")
                processed_weather = p.get("processed_weather") or p.get("weather")
                print("--------------------------------------------")
                print(f"Zone: {getattr(zone, 'name', 'Unknown')}")
                if processed_weather:
                    pw_dict = _obj_to_dict(processed_weather)
                    try:
                        pretty = json.dumps(pw_dict, indent=2, default=str)
                    except TypeError:
                        pretty = str(pw_dict)
                    print(pretty)
                else:
                    print("No processed data for this zone.")

            # ----------------------------------------------------------
            # 8.3 Predictions + Alerts
            # ----------------------------------------------------------
            print("\n🔮 Generating predictions & alerts...")
            predictions, alerts = await prediction_orchestrator.predict_all_zones(processed_data)

            # ----------------------------------------------------------
            # 8.4 Save Predictions
            # ----------------------------------------------------------
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
                        json.dumps(pred.risk_factors.model_dump()),
                        json.dumps(pred.recommended_actions),
                    )

            # ----------------------------------------------------------
            # 8.5 Save Alerts
            # ----------------------------------------------------------
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
                        alert.priority,
                    )

            # ----------------------------------------------------------
            # 8.6 Show Summary of this Cycle
            # ----------------------------------------------------------
            print("\n📊 PREDICTIONS (this cycle)")
            for pred in predictions:
                print("--------------------------------------------")
                print(f"Zone: {pred.zone.name}")
                print(f"Risk Score: {pred.risk_score:.2f}")
                print(f"Severity: {pred.severity_level.value}")
                print(f"Confidence: {pred.confidence:.2f}")
                print(f"ETA (hours): {pred.time_to_impact_hours}")
                print(f"Affected Area (km²): {pred.affected_area_km2}")

            print("\n🚨 ALERTS (this cycle)")
            if not alerts:
                print("No alerts generated.")
            for alert in alerts:
                print("--------------------------------------------")
                print(f"[{alert.severity.value}] {alert.alert_type.value}")
                print(f"Zone: {alert.zone.name}")
                print(f"Priority: {alert.priority}")
                print(f"Message: {alert.message}")

            print("\n✅ Cycle finished. Sleeping 30 seconds...")
            print("   Press Ctrl+C to stop.\n")
            await asyncio.sleep(30)

    except KeyboardInterrupt:
        print("\n🛑 Stopped by user (Ctrl+C). Shutting down gracefully...")
    finally:
        await pool.close()
        print("🔌 PostgreSQL connection pool closed.")
        print("👋 Agent stopped.")


def run():
    return asyncio.run(main())


# if __name__ == "__main__":
#     asyncio.run(main())
