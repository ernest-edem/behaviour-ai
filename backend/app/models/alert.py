from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.db import Base


class HealthAlert(Base):
    __tablename__ = "health_alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    alert_type = Column(String)  # risk_spike, health_drop, anomaly
    message = Column(String)

    severity = Column(String)  # low, medium, high, critical

    health_score = Column(Float)
    risk_score = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())