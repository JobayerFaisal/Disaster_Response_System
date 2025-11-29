from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Existing Routers
from backend.api.routes.weather import router as weather_router
from backend.api.routes.predictions import router as predictions_router
from backend.api.routes.danger_zones import router as danger_router
from backend.api.routes.agents import router as agents_router
from backend.api.routes.zones import router as zones_router

# New Router for Manual Report
from backend.api.routes.manual_report import router as manual_report_router  # New import

# WebSocket alerts
from backend.api.websocket.alerts import alerts_ws

# Create FastAPI app instance
app = FastAPI(title="Disaster AI API", version="1.0.0")

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include Routers
app.include_router(weather_router, prefix="/weather", tags=["Weather"])
app.include_router(predictions_router, prefix="/predictions", tags=["Predictions"])
app.include_router(danger_router, prefix="/danger-zones", tags=["Danger Zones"])
app.include_router(agents_router, prefix="/agents", tags=["Agents"])
app.include_router(zones_router, prefix="/zones", tags=["Zones"])

# Include the Manual Report Router
app.include_router(manual_report_router, prefix="/manual-report", tags=["Manual Reports"])  # New route for manual reports

# WebSocket alerts route
app.add_api_websocket_route("/ws/alerts", alerts_ws)
