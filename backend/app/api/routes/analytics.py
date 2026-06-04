from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.services.analytics_service import AnalyticsService


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)

analytics_service = AnalyticsService()


# =====================================================
# HEALTH TIMELINE (PHASE 6 CORE API)
# =====================================================

@router.get("/timeline/{user_id}")
def get_timeline(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Returns:
    - Patient longitudinal timeline
    - Risk trend analysis
    """

    result = analytics_service.get_health_timeline(
        db=db,
        user_id=user_id
    )

    return result