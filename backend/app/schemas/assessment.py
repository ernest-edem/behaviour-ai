from pydantic import BaseModel
from typing import List


class HealthAssessmentRequest(BaseModel):
    sleep_hours: float
    exercise_minutes: int
    water_intake_liters: float

    stress_level: int
    screen_time_hours: float

    smoker: bool
    alcohol_use: bool

    diet_quality: int
    fruits_per_day: int
    vegetables_per_day: int

    symptoms: List[str]