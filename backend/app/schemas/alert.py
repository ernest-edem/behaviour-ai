from pydantic import BaseModel
from datetime import datetime


class AlertResponse(BaseModel):
    id: int
    alert_type: str
    title: str
    message: str
    risk_score: float | None = None
    health_score: float | None = None
    severity: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True