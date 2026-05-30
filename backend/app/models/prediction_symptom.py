from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database.db import Base


class PredictionSymptom(Base):
    __tablename__ = "prediction_symptoms"

    # =====================================
    # PRIMARY KEY
    # =====================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================
    # RELATION TO PREDICTION
    # =====================================

    prediction_id = Column(
        Integer,
        ForeignKey(
            "predictions.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    # =====================================
    # SYMPTOM
    # =====================================

    symptom = Column(
        String(255),
        nullable=False
    )

    # =====================================
    # RELATIONSHIPS
    # =====================================

    prediction = relationship(
        "Prediction",
        back_populates="symptoms"
    )