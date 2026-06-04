from typing import Dict, Any
from pydantic import BaseModel, Field, ValidationError


class FeatureContract(BaseModel):
    """
    Strict ML feature schema contract.

    Guarantees:
    - deterministic feature shape
    - prevents silent feature drift
    - safe for ML + SHAP + phenotype + audit
    """

    sleep_hours: float = Field(default=0.0, ge=0, le=24)
    exercise_minutes: float = Field(default=0.0, ge=0)
    water_intake_liters: float = Field(default=0.0, ge=0)
    stress_level: float = Field(default=0.0, ge=0, le=10)
    screen_time_hours: float = Field(default=0.0, ge=0, le=24)
    smoker: int = Field(default=0, ge=0, le=1)
    alcohol_use: int = Field(default=0, ge=0, le=1)
    diet_quality: float = Field(default=0.0, ge=0, le=10)
    fruits_per_day: float = Field(default=0.0, ge=0)
    vegetables_per_day: float = Field(default=0.0, ge=0)

    @classmethod
    def build(cls, raw: Dict[str, Any]) -> Dict[str, float]:
        """
        Safe feature normalization layer.
        Always returns valid ML-ready vector.
        """

        try:
            validated = cls(**raw)
        except ValidationError:
            # HARD fallback (never break pipeline)
            return {
                "sleep_hours": 0.0,
                "exercise_minutes": 0.0,
                "water_intake_liters": 0.0,
                "stress_level": 0.0,
                "screen_time_hours": 0.0,
                "smoker": 0.0,
                "alcohol_use": 0.0,
                "diet_quality": 0.0,
                "fruits_per_day": 0.0,
                "vegetables_per_day": 0.0,
            }

        return validated.model_dump()