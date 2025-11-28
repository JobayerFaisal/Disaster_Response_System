import os
import time
import traceback
from datetime import datetime

# Shared utilities
from backend.shared.db import get_db_connection
from backend.shared.logger import log_info, log_error

# Agents
from backend.agents.environmental_agent.run import run as run_environment
from backend.agents.danger_zone_agent.run import run as run_danger_zones

# from backend.agents.river_agent.run import run as run_river
# from backend.agents.flood_prediction_agent.run import run as run_flood_prediction
# from backend.agents.danger_zone_agent.run import run as run_danger_zones
# from backend.agents.notification_agent.run import run as run_notification


class AgentCore:
    def __init__(self):
        self.db = get_db_connection()

    def record_agent_status(self, agent_name, status, message):
        """Save agent execution state in PostgreSQL"""
        cursor = self.db.cursor()
        cursor.execute(
            """
            INSERT INTO agent_logs (timestamp, agent_name, status, message)
            VALUES (%s, %s, %s, %s)
            """,
            (datetime.utcnow(), agent_name, status, message),
        )
        self.db.commit()

    def safe_run(self, agent_fn, agent_name):
        """Runs an agent safely with exception handling + logging."""
        log_info(f"▶ Running {agent_name}...")

        try:
            result = agent_fn()  # environmental agent is sync-wrapper
            self.record_agent_status(agent_name, "success", "Completed")
            log_info(f"✔ {agent_name} finished successfully")
            return result

        except Exception as e:
            error_msg = f"{agent_name} failed: {str(e)}\n{traceback.format_exc()}"
            log_error(error_msg)
            self.record_agent_status(agent_name, "failed", error_msg)
            return None

    def run_pipeline(self):
        """The full multi-agent pipeline execution"""
        log_info("🚀 Starting AI Disaster Intelligence Pipeline")
        start_time = time.time()

        results = {}

        # 1️⃣ Environmental Agent
        results["environment"] = self.safe_run(run_environment, "environmental_agent")

        # 4️⃣ Danger Zone Detection Agent
        results["danger_zones"] = self.safe_run(run_danger_zones, "danger_zone_agent")


        # 2️⃣ River Agent
        # results["river"] = self.safe_run(run_river, "river_agent")

        # 3️⃣ Flood Prediction Agent
        # results["prediction"] = self.safe_run(run_flood_prediction, "flood_prediction_agent")

        # 4️⃣ Danger Zone Detection Agent
        # results["danger_zones"] = self.safe_run(run_danger_zones, "danger_zone_agent")

        # 5️⃣ Notification Agent
        # results["notifications"] = self.safe_run(run_notification, "notification_agent")

        self.db.close()  # Close PostgreSQL connection

        log_info(f"🏁 Pipeline completed in {time.time() - start_time:.2f}s")
        return results


def run():
    """Convenience method"""
    core = AgentCore()
    return core.run_pipeline()


if __name__ == "__main__":
    run()
