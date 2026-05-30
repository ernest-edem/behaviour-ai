from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.db import Base


class HealthReport(Base):
    __tablename__ = "health_reports"

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
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    # =====================================
    # REPORT SCORES
    # =====================================

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

    # =====================================
    # AI ASSESSMENT
    # =====================================

    predicted_disease = Column(
        String(255),
        nullable=True
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
    # REPORT CONTENT
    # =====================================

    summary = Column(
        Text,
        nullable=True
    )

    recommendations = Column(
        Text,
        nullable=True
    )

    # =====================================
    # SYSTEM INFO
    # =====================================

    report_version = Column(
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
        back_populates="health_reports"
    )