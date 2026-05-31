from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TimelinePoint(BaseModel):
    date: str
    health_score: float
    risk_score: float
    risk_level: Optional[str] = None
    predicted_disease: Optional[str] = None


class TimelineSummary(BaseModel):
    avg_health_score: float
    avg_risk_score: float
    trend: str
    risk_trend: str


class HealthTimelineResponse(BaseModel):
    user_id: int
    period: str
    data_points: int
    timeline: List[TimelinePoint]
    summary: TimelineSummary