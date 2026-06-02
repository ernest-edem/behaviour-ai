from sqlalchemy.orm import Session

from app.models.prediction import Prediction


def get_user_prediction_history(
    db: Session,
    user_id: int
):
    predictions = (
        db.query(Prediction)
        .filter(
            Prediction.user_id == user_id
        )
        .order_by(
            Prediction.created_at.asc()
        )
        .all()
    )

    history = []

    for prediction in predictions:

        history.append({
            "id": prediction.id,
            "date": (
                prediction.created_at.strftime(
                    "%Y-%m-%d"
                )
                if prediction.created_at
                else None
            ),
            "health_score": prediction.health_score,
            "risk_score": prediction.risk_score,
            "ai_confidence": prediction.ai_confidence,
            "predicted_disease": prediction.predicted_disease,
            "risk_level": prediction.risk_level,
            "urgency": prediction.urgency,
        })

    return history