from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    Float,
    DateTime,
    Text,
    JSON
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.db import Base


class Prediction(Base):
    __tablename__ = "predictions"

    # ==================================================
    # PRIMARY KEY
    # ==================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # ==================================================
    # USER RELATION
    # ==================================================

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # ==================================================
    # CANONICAL PREDICTION FIELDS
    # ==================================================

    predicted_condition = Column(
        String(255),
        nullable=False,
        index=True
    )

    confidence_score = Column(
        Float,
        default=0.0
    )

    # ==================================================
    # BACKWARD COMPATIBILITY
    # ==================================================

    predicted_disease = Column(
        String(255),
        nullable=False
    )

    ai_confidence = Column(
        Float,
        default=0.0
    )

    # ==================================================
    # HEALTH METRICS
    # ==================================================

    health_score = Column(
        Float,
        default=0.0
    )

    risk_score = Column(
        Float,
        default=0.0
    )

    risk_level = Column(
        String(50),
        default="Low"
    )

    urgency = Column(
        String(50),
        default="Low"
    )

    # ==================================================
    # BEHAVIORAL ANALYTICS
    # ==================================================

    lifestyle_score = Column(
        Float,
        default=0.0
    )

    behavior_score = Column(
        Float,
        default=0.0
    )

    behavioral_phenotype = Column(
        String(255),
        nullable=True
    )

    # ==================================================
    # MODEL OUTPUT
    # ==================================================

    recommendation = Column(
        Text,
        nullable=True
    )

    explanation = Column(
        Text,
        nullable=True
    )

    # ==================================================
    # EXPLAINABILITY
    # ==================================================

    disease_probabilities = Column(
        JSON,
        nullable=True
    )

    shap_values = Column(
        JSON,
        nullable=True
    )

    feature_contributions = Column(
        JSON,
        nullable=True
    )

    # ==================================================
    # MODEL METADATA
    # ==================================================

    prediction_source = Column(
        String(50),
        nullable=False,
        default="rule_engine"
    )

    model_name = Column(
        String(255),
        nullable=True
    )

    model_type = Column(
        String(255),
        nullable=True
    )

    model_version = Column(
        String(100),
        nullable=True
    )

    # ==================================================
    # AUDIT
    # ==================================================

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # ==================================================
    # RELATIONSHIPS
    # ==================================================

    user = relationship(
        "User",
        back_populates="predictions"
    )

    symptoms = relationship(
        "PredictionSymptom",
        back_populates="prediction",
        cascade="all, delete-orphan"
    )

    # ==================================================
    # HELPERS
    # ==================================================

    @property
    def display_condition(self) -> str:
        return (
            self.predicted_condition
            or self.predicted_disease
        )

    @property
    def display_confidence(self) -> float:
        return (
            self.confidence_score
            if self.confidence_score is not None
            else self.ai_confidence
        )

    @property
    def canonical_condition(self) -> str:
        return self.display_condition

    @property
    def canonical_confidence(self) -> float:
        return self.display_confidence