from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes.weather import router as weather_router
from backend.api.routes.predictions import router as predictions_router
from backend.api.routes.danger_zones import router as danger_router
from backend.api.routes.agents import router as agents_router
from backend.api.routes.zones import router as zones_router

from backend.api.websocket.alerts import alerts_ws

app = FastAPI(title="Disaster AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(weather_router, prefix="/weather", tags=["Weather"])
app.include_router(predictions_router, prefix="/predictions", tags=["Predictions"])
app.include_router(danger_router, prefix="/danger-zones", tags=["Danger Zones"])
app.include_router(agents_router, prefix="/agents", tags=["Agents"])
app.include_router(zones_router, prefix="/zones", tags=["Zones"])

# WebSocket alerts
app.add_api_websocket_route("/ws/alerts", alerts_ws)
