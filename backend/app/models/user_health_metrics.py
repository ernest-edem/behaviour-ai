from sqlalchemy import Column, Integer, Float, ForeignKey
from app.database.db import Base


class UserHealthMetrics(Base):
    __tablename__ = "user_health_metrics"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    average_health_score = Column(Float)
    average_risk_score = Column(Float)

    best_health_score = Column(Float)
    worst_health_score = Column(Float)

    trend_percentage = Column(Float)

    total_assessments = Column(Integer)