from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.health_alert import HealthAlert

router = APIRouter(
    prefix="/alerts",
    tags=["Health Alerts"]
)


@router.get("/{user_id}")
def get_alerts(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 🔒 Security check
    if current_user.id != user_id:
        return {"error": "Unauthorized access"}

    # 📊 FETCH STORED ALERTS (NOT GENERATED)
    alerts = (
        db.query(HealthAlert)
        .filter(HealthAlert.user_id == user_id)
        .order_by(HealthAlert.created_at.desc())
        .all()
    )

    return {
        "user_id": user_id,
        "count": len(alerts),
        "alerts": alerts
    }