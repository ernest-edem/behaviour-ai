from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from datetime import datetime

from app.database.db import Base


class RiskTrend(Base):
    __tablename__ = "risk_trends"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    disease_name = Column(String(100))
    risk_score = Column(Float, nullable=False)

    trend_direction = Column(String(20))

    moving_average_7d = Column(Float)
    moving_average_30d = Column(Float)

    volatility_score = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)