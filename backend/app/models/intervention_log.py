from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Text
from datetime import datetime

from app.database.db import Base


class InterventionLog(Base):
    __tablename__ = "intervention_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    intervention_type = Column(String(100))
    trigger_source = Column(String(100))

    description = Column(Text)
    effectiveness_score = Column(Float)

    status = Column(String(20), default="active")

    created_at = Column(DateTime, default=datetime.utcnow)