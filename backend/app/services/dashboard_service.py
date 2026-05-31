from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.prediction import Prediction
from app.models.lifestyle_log import LifestyleLog


def get_health_dashboard(db: Session, user_id: int):

    predictions = db.query(Prediction)\
        .filter(Prediction.user_id == user_id)\
        .order_by(Prediction.created_at.asc())\
        .all()

    if not predictions:
        return {
            "message": "No data available"
        }

    # -------------------------
    # BASIC METRICS
    # -------------------------
    avg_health = sum(p.health_score for p in predictions) / len(predictions)
    avg_risk = sum(p.risk_score for p in predictions) / len(predictions)

    # -------------------------
    # MOST COMMON DISEASE
    # -------------------------
    disease_counts = {}
    for p in predictions:
        disease_counts[p.predicted_disease] = disease_counts.get(p.predicted_disease, 0) + 1

    most_common_disease = max(disease_counts, key=disease_counts.get)

    # -------------------------
    # RISK TREND (simple timeline)
    # -------------------------
    risk_trend = [
        {
            "date": p.created_at,
            "risk_score": p.risk_score,
            "health_score": p.health_score
        }
        for p in predictions
    ]

    # -------------------------
    # LATEST RECORD
    # -------------------------
    latest = predictions[-1]

    return {
        "average_health_score": round(avg_health, 2),
        "average_risk_score": round(avg_risk, 2),
        "most_common_disease": most_common_disease,
        "latest_risk_level": latest.risk_level,
        "latest_urgency": latest.urgency,
        "risk_trend": risk_trend
    }