from sqlalchemy import (
    Column,
    Integer,
    Float,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.db import Base


class LifestyleLog(Base):
    __tablename__ = "lifestyle_logs"

    # =====================================
    # PRIMARY KEY
    # =====================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

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
    # SLEEP
    # =====================================

    sleep_hours = Column(
        Float,
        nullable=True
    )

    # =====================================
    # PHYSICAL ACTIVITY
    # =====================================

    exercise_minutes = Column(
        Integer,
        nullable=True
    )

    # =====================================
    # HYDRATION
    # =====================================

    water_intake_liters = Column(
        Float,
        nullable=True
    )

    # =====================================
    # MENTAL HEALTH
    # =====================================

    stress_level = Column(
        Integer,
        nullable=True
    )  # 1 - 10

    # =====================================
    # DIGITAL BEHAVIOR
    # =====================================

    screen_time_hours = Column(
        Float,
        nullable=True
    )

    # =====================================
    # SUBSTANCE USE
    # =====================================

    smoker = Column(
        Boolean,
        default=False
    )

    alcohol_use = Column(
        Boolean,
        default=False
    )

    # =====================================
    # NUTRITION
    # =====================================

    diet_quality = Column(
        Integer,
        nullable=True
    )  # 1 - 10

    fruits_per_day = Column(
        Integer,
        nullable=True
    )

    vegetables_per_day = Column(
        Integer,
        nullable=True
    )

    # =====================================
    # BEHAVIOUR AI SCORES
    # =====================================

    lifestyle_score = Column(
        Float,
        nullable=True
    )

    risk_score = Column(
        Float,
        nullable=True
    )

    # =====================================
    # TIMESTAMPS
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
        back_populates="lifestyle_logs"
    )