from pydantic import BaseModel, Field, field_validator
from typing import Optional


class FeatureSchema(BaseModel):
    """
    Production-grade ML feature contract.

    Guarantees:
    - No missing values
    - Safe defaults
    - Strict numeric normalization
    - Prevents NaN/None propagation into ML models
    """

    sleep_hours: float = Field(default=7.0, ge=0, le=24)
    exercise_minutes: float = Field(default=30.0, ge=0, le=600)
    water_intake_liters: float = Field(default=2.0, ge=0, le=10)

    stress_level: float = Field(default=3.0, ge=0, le=10)
    screen_time_hours: float = Field(default=4.0, ge=0, le=24)

    smoker: float = Field(default=0.0, ge=0, le=1)
    alcohol_use: float = Field(default=0.0, ge=0, le=1)

    diet_quality: float = Field(default=5.0, ge=0, le=10)
    fruits_per_day: float = Field(default=2.0, ge=0, le=20)
    vegetables_per_day: float = Field(default=2.0, ge=0, le=20)

    # ==========================================
    # VALIDATION LAYER (CRITICAL FOR ML SAFETY)
    # ==========================================

    @field_validator("*", mode="before")
    @classmethod
    def _coerce_numeric(cls, v):
        """
        Forces safe numeric conversion.
        Prevents: strings, None, NaN, bad payloads
        """
        if v is None:
            return None

        try:
            # handle boolean explicitly
            if isinstance(v, bool):
                return float(int(v))

            value = float(v)

            # NaN protection
            if value != value:  # NaN check
                return None

            return value
        except Exception:
            return None

    @field_validator("*", mode="after")
    @classmethod
    def _apply_fallbacks(cls, v, info):
        """
        Ensures no None leaks into ML layer.
        """
        if v is None:
            defaults = {
                "sleep_hours": 7.0,
                "exercise_minutes": 30.0,
                "water_intake_liters": 2.0,
                "stress_level": 3.0,
                "screen_time_hours": 4.0,
                "smoker": 0.0,
                "alcohol_use": 0.0,
                "diet_quality": 5.0,
                "fruits_per_day": 2.0,
                "vegetables_per_day": 2.0,
            }
            return defaults.get(info.field_name, 0.0)

        return v

    class Config:
        extra = "ignore"
        validate_assignment = True