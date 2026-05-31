from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

# =====================================
# INPUT
# =====================================

class PredictionRequest(BaseModel):
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


# =====================================
# OUTPUT
# =====================================

class PredictionResponse(BaseModel):
    health_score: float

    risk_score: float

    ai_confidence: float

    predicted_disease: str

    risk_level: str

    urgency: str

    explanation: List[str]

    recommendation: str


# =====================================
# HISTORY
# =====================================

class PredictionHistoryResponse(BaseModel):
    id: int

    predicted_disease: str

    health_score: float

    risk_score: float

    ai_confidence: float

    risk_level: str

    urgency: str

    created_at: datetime

    class Config:
        from_attributes = True

class PredictionHistoryItem(BaseModel):
    id: int
    predicted_disease: str
    health_score: float
    risk_score: float
    ai_confidence: float
    risk_level: str
    urgency: str
    created_at: datetime

    class Config:
        from_attributes = True


class PredictionHistoryResponse(BaseModel):
    history: List[PredictionHistoryItem]
    total: int