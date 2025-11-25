from sqlalchemy import Column, Integer, JSON, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from core.db import Base

class SimulationDay(Base):
    __tablename__ = "simulation_days"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(Integer, nullable=False)

    weather = Column(JSONB)
    river = Column(JSONB)
    flood_map = Column(JSONB)
    drone_analysis = Column(JSONB)
    infrastructure = Column(JSONB)

    social_media_sos = Column(JSONB)
    hotline_sos = Column(JSONB)
    triaged_sos = Column(JSONB)

    routes = Column(JSONB)
    resource_plan = Column(JSONB)
    disease_risk = Column(JSONB)

    coordinator = Column(JSONB)

    created_at = Column(DateTime, server_default=func.now())
