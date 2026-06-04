from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from datetime import datetime

from app.database.db import Base


class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    prediction_id = Column(Integer, ForeignKey("predictions.id"))

    predicted_disease = Column(String(100))
    risk_score = Column(Float, nullable=False)
    health_score = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)

    model_version = Column(String(50))

    created_at = Column(DateTime, default=datetime.utcnow)