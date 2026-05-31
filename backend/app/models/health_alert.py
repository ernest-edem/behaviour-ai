from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.database.db import Base


class HealthAlert(Base):
    __tablename__ = "health_alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    alert_type = Column(String)  # critical, warning, info
    title = Column(String)
    message = Column(String)

    risk_score = Column(Float)
    health_score = Column(Float)

    severity = Column(String)  # high, medium, low

    created_at = Column(DateTime(timezone=True), server_default=func.now())