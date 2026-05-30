from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.db import Base


class DiseaseRiskHistory(Base):
    __tablename__ = "disease_risk_history"

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
    # DISEASE INFORMATION
    # =====================================

    disease_name = Column(
        String(255),
        nullable=False
    )

    risk_score = Column(
        Float,
        default=0
    )

    risk_level = Column(
        String(50),
        default="Low"
    )

    ai_confidence = Column(
        Float,
        default=0
    )

    # =====================================
    # TIMESTAMP
    # =====================================

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================
    # RELATIONSHIPS
    # =====================================

    user = relationship(
        "User",
        back_populates="disease_risk_history"
    )