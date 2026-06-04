from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict


# ==================================================
# INPUT
# ==================================================

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


# ==================================================
# CANONICAL PREDICTION RESPONSE
# ==================================================

class PredictionResponse(BaseModel):
    prediction_id: Optional[int] = None

    health_score: float
    risk_score: float

    ai_confidence: float
    predicted_disease: str

    risk_level: str
    urgency: str

    behavioral_phenotype: Optional[str] = None

    disease_probabilities: Dict[str, float]

    explanations: List[str]

    recommendation: str

    prediction_source: str
    model_version: Optional[str] = None

    # ----------------------------------------------
    # Backward compatibility
    # ----------------------------------------------

    ai_confidence: Optional[float] = None
    predicted_disease: Optional[str] = None
    explanation: Optional[List[str]] = None


# ==================================================
# HISTORY ITEM
# ==================================================

class PredictionHistoryItem(BaseModel):
    id: int

    predicted_disease: Optional[str] = None
    ai_confidence: Optional[float] = None

    predicted_disease: str
    ai_confidence: float

    health_score: float
    risk_score: float

    risk_level: str
    urgency: str

    model_version: Optional[str] = None
    prediction_source: Optional[str] = None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ==================================================
# HISTORY RESPONSE
# ==================================================

class PredictionHistoryResponse(BaseModel):
    history: List[PredictionHistoryItem]
    total: int


# ==================================================
# DATABASE SERIALIZATION
# ==================================================

class PredictionDBResponse(BaseModel):
    id: int

    user_id: int

    predicted_disease: Optional[str] = None
    ai_confidence: Optional[float] = None

    predicted_disease: str
    ai_confidence: float

    health_score: float
    risk_score: float

    risk_level: str
    urgency: str

    behavioral_phenotype: Optional[str] = None

    disease_probabilities: Optional[
        Dict[str, float]
    ] = None

    recommendation: Optional[str] = None
    explanation: Optional[str] = None

    prediction_source: Optional[str] = None

    model_name: Optional[str] = None
    model_type: Optional[str] = None
    model_version: Optional[str] = None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )