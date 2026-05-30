from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.db import Base


class SymptomLog(Base):
    __tablename__ = "symptom_logs"

    # ==========================
    # PRIMARY KEY
    # ==========================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # ==========================
    # USER
    # ==========================

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    # ==========================
    # SYMPTOM DATA
    # ==========================

    symptom_name = Column(
        String(100),
        nullable=False
    )

    severity = Column(
        Integer,
        nullable=True
    )

    duration_days = Column(
        Integer,
        nullable=True
    )

    notes = Column(
        String(500),
        nullable=True
    )

    # ==========================
    # TIMESTAMP
    # ==========================

    logged_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # ==========================
    # RELATIONSHIP
    # ==========================

    user = relationship(
        "User",
        back_populates="symptom_logs"
    )