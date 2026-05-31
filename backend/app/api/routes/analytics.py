from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database.db import get_db
from app.models.prediction import Prediction
from app.schemas.timeline import HealthTimelineResponse

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/health-timeline/{user_id}", response_model=HealthTimelineResponse)
def get_health_timeline(
    user_id: int,
    period: str = Query("30d"),
    db: Session = Depends(get_db)
):
    # ----------------------------
    # 1. Date filtering
    # ----------------------------
    days = int(period.replace("d", ""))
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    predictions = (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id)
        .filter(Prediction.created_at >= cutoff_date)
        .order_by(Prediction.created_at.asc())
        .all()
    )

    # ----------------------------
    # 2. Build timeline
    # ----------------------------
    timeline = []
    total_health = 0
    total_risk = 0

    for p in predictions:
        timeline.append({
            "date": p.created_at.strftime("%Y-%m-%d"),
            "health_score": p.health_score,
            "risk_score": p.risk_score,
            "risk_level": p.risk_level,
            "predicted_disease": p.predicted_disease
        })

        total_health += p.health_score
        total_risk += p.risk_score

    count = len(predictions) or 1

    avg_health = total_health / count
    avg_risk = total_risk / count

    # ----------------------------
    # 3. Simple trend logic (upgrade later to ML)
    # ----------------------------
    if len(predictions) >= 2:
        trend = (
            "improving"
            if predictions[-1].health_score > predictions[0].health_score
            else "declining"
        )
    else:
        trend = "stable"

    risk_trend = (
        "improving"
        if avg_risk < 50
        else "rising"
    )

    # ----------------------------
    # 4. Response
    # ----------------------------
    return {
        "user_id": user_id,
        "period": period,
        "data_points": len(timeline),
        "timeline": timeline,
        "summary": {
            "avg_health_score": round(avg_health, 2),
            "avg_risk_score": round(avg_risk, 2),
            "trend": trend,
            "risk_trend": risk_trend
        }
    }