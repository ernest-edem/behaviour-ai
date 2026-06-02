from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func
from app.database.db import Base


class HealthAlert(Base):
    __tablename__ = "health_alerts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    alert_type = Column(String)

    title = Column(String)

    message = Column(String)

    risk_score = Column(Float)

    health_score = Column(Float)

    severity = Column(String)

    is_read = Column(
        Boolean,
        default=False,
        nullable=False
    )

    read_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )