from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.prediction import Prediction

from app.services.insight_service import generate_health_insights

router = APIRouter(
    prefix="/insights",
    tags=["AI Insights"]
)


@router.get("/{user_id}")
def get_insights(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.id != user_id:
        return {"error": "Unauthorized access"}

    predictions = (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id)
        .order_by(Prediction.created_at.asc())
        .all()
    )

    insights = generate_health_insights(predictions)

    return {
        "user_id": user_id,
        "insights": insights
    }