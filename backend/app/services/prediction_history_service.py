from sqlalchemy.orm import Session
from app.models.prediction import Prediction


def get_user_prediction_history(db: Session, user_id: int):
    predictions = (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id)
        .order_by(Prediction.created_at.desc())
        .all()
    )

    return predictions