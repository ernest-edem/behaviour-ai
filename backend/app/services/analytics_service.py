from sqlalchemy.orm import Session
from app.models.prediction import Prediction


def get_health_timeline(db: Session, user_id: int):
    records = (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id)
        .order_by(Prediction.created_at.asc())
        .all()
    )

    timeline = []

    for r in records:
        timeline.append({
            "created_at": r.created_at,
            "health_score": r.health_score,
            "risk_score": r.risk_score,
            "ai_confidence": r.ai_confidence
        })

    return {
        "user_id": user_id,
        "timeline": timeline
    }