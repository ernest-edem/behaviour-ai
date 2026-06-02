from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.db import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.health_alert import HealthAlert

router = APIRouter(
    prefix="/alerts",
    tags=["Health Alerts"]
)


@router.put("/{alert_id}/read")
def mark_alert_read(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    alert = (
        db.query(HealthAlert)
        .filter(
            HealthAlert.id == alert_id,
            HealthAlert.user_id == current_user.id
        )
        .first()
    )

    if not alert:
        return {"error": "Alert not found"}

    alert.is_read = True

    db.commit()

    return {
        "success": True,
        "message": "Alert marked as read"
    }


@router.get("/unread/count")
def unread_alert_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    count = (
        db.query(HealthAlert)
        .filter(
            HealthAlert.user_id == current_user.id,
            HealthAlert.is_read == False
        )
        .count()
    )

    return {
        "unread_alerts": count
    }
    


@router.get("/{user_id}")
def get_alerts(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized access"
        )

    alerts = (
        db.query(HealthAlert)
        .filter(
            HealthAlert.user_id == user_id
        )
        .order_by(
            HealthAlert.created_at.desc()
        )
        .all()
    )

    unread_count = (
        db.query(HealthAlert)
        .filter(
            HealthAlert.user_id == user_id,
            HealthAlert.is_read == False
        )
        .count()
    )

    return {
        "user_id": user_id,
        "count": len(alerts),
        "unread_count": unread_count,
        "alerts": alerts
    }


@router.patch("/{alert_id}/read")
def mark_alert_read(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    alert = (
        db.query(HealthAlert)
        .filter(
            HealthAlert.id == alert_id,
            HealthAlert.user_id == current_user.id
        )
        .first()
    )

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    alert.is_read = True

    db.commit()

    return {
        "success": True,
        "message": "Alert marked as read"
    }