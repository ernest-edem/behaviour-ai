from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    Float,
    DateTime,
    Text
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.db import Base


class Prediction(Base):
    __tablename__ = "predictions"

    # =====================================
    # PRIMARY KEY
    # =====================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================
    # USER RELATION
    # =====================================

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    # =====================================
    # AI RESULT
    # =====================================

    predicted_disease = Column(
        String(255),
        nullable=False
    )

    health_score = Column(
        Float,
        default=0
    )

    risk_score = Column(
        Float,
        default=0
    )

    ai_confidence = Column(
        Float,
        default=0
    )

    risk_level = Column(
        String(50),
        default="Low"
    )

    urgency = Column(
        String(50),
        default="Low"
    )

    # =====================================
    # BEHAVIOURAL ANALYSIS
    # =====================================

    lifestyle_score = Column(
        Float,
        default=0
    )

    behavior_score = Column(
        Float,
        default=0
    )

    # =====================================
    # AI OUTPUT
    # =====================================

    recommendation = Column(
        Text,
        nullable=True
    )

    explanation = Column(
        Text,
        nullable=True
    )

    # =====================================
    # SYSTEM
    # =====================================

    model_version = Column(
        String(50),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================
    # RELATIONSHIPS
    # =====================================

    user = relationship(
        "User",
        back_populates="predictions"
    )

    symptoms = relationship(
        "PredictionSymptom",
        back_populates="prediction",
        cascade="all, delete-orphan"
    )