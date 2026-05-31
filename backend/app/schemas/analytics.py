from pydantic import BaseModel
from datetime import datetime
from typing import List


class TimelinePoint(BaseModel):
    created_at: datetime
    health_score: float
    risk_score: float
    ai_confidence: float


class HealthTimelineResponse(BaseModel):
    user_id: int
    timeline: List[TimelinePoint]