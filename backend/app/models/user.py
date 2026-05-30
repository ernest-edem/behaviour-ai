from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Boolean
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.db import Base


class User(Base):
    __tablename__ = "users"

    # =====================================
    # PRIMARY KEY
    # =====================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================
    # ACCOUNT INFORMATION
    # =====================================

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    # =====================================
    # DEMOGRAPHIC DATA
    # =====================================

    age = Column(
        Integer,
        nullable=True
    )

    gender = Column(
        String(20),
        nullable=True
    )

    country = Column(
        String(100),
        nullable=True
    )

    occupation = Column(
        String(100),
        nullable=True
    )

    # =====================================
    # HEALTH PROFILE
    # =====================================

    height_cm = Column(
        Float,
        nullable=True
    )

    weight_kg = Column(
        Float,
        nullable=True
    )

    bmi = Column(
        Float,
        nullable=True
    )

    blood_group = Column(
        String(10),
        nullable=True
    )

    # =====================================
    # ACCOUNT STATUS
    # =====================================

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    is_verified = Column(
        Boolean,
        default=False,
        nullable=False
    )

    # =====================================
    # TIMESTAMPS
    # =====================================

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # =====================================
    # RELATIONSHIPS
    # =====================================

    predictions = relationship(
        "Prediction",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    lifestyle_logs = relationship(
        "LifestyleLog",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    symptom_logs = relationship(
        "SymptomLog",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    health_reports = relationship(
        "HealthReport",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    disease_risk_history = relationship(
        "DiseaseRiskHistory",
        back_populates="user",
        cascade="all, delete-orphan"
    )