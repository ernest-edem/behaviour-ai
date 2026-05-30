from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey,
    DateTime
)
from sqlalchemy.sql import func

from app.database.db import Base


class HealthProfile(Base):
    __tablename__ = "health_profiles"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    height_cm = Column(Float)

    weight_kg = Column(Float)

    bmi = Column(Float)

    blood_group = Column(String(10))

    family_history = Column(String(1000))

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )