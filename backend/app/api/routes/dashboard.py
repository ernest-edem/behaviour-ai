from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.core.dependencies import get_current_user
from app.models.user import User

from app.services.dashboard_service import get_health_dashboard

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/{user_id}")
def health_dashboard(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # ensure user can only access their own data
    if current_user.id != user_id:
        return {"error": "Unauthorized access"}

    return get_health_dashboard(db, user_id)