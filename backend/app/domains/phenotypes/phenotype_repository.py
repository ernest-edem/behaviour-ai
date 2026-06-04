from typing import Dict, Any, List, Optional

from sqlalchemy.orm import Session

from app.models.behavioral_profile import BehavioralProfile
from app.models.behavioral_profile_history import BehavioralProfileHistory


class PhenotypeRepository:
    """
    Persistence layer for Phase 4 Behavioral Phenotyping.

    Responsibilities:
    - Store current phenotype
    - Store history snapshots
    - Retrieve user behavioral evolution
    """

    # ==================================================
    # CREATE CURRENT PROFILE
    # ==================================================

    def create_profile(
        self,
        db: Session,
        user_id: int,
        phenotype: str,
        risk_score: float,
        confidence: float,
        model_version: str,
        extra: Optional[Dict[str, Any]] = None
    ) -> BehavioralProfile:

        profile = BehavioralProfile(
            user_id=user_id,
            phenotype=phenotype,
            risk_score=risk_score,
            confidence=confidence,
            model_version=model_version,

            stability_score=extra.get("stability_score") if extra else None,
            adherence_score=extra.get("adherence_score") if extra else None,
            stress_index=extra.get("stress_index") if extra else None,
            lifestyle_score=extra.get("lifestyle_score") if extra else None,
        )

        db.add(profile)
        db.commit()
        db.refresh(profile)

        return profile

    # ==================================================
    # ADD HISTORY SNAPSHOT
    # ==================================================

    def add_history(
        self,
        db: Session,
        user_id: int,
        profile_id: int,
        phenotype: str,
        snapshot: Dict[str, Any],
    ) -> BehavioralProfileHistory:

        history = BehavioralProfileHistory(
            user_id=user_id,
            profile_id=profile_id,
            phenotype=phenotype,
            snapshot=snapshot,
        )

        db.add(history)
        db.commit()
        db.refresh(history)

        return history

    # ==================================================
    # GET CURRENT PROFILE
    # ==================================================

    def get_latest_profile(
        self,
        db: Session,
        user_id: int
    ) -> Optional[BehavioralProfile]:

        return (
            db.query(BehavioralProfile)
            .filter(BehavioralProfile.user_id == user_id)
            .order_by(BehavioralProfile.created_at.desc())
            .first()
        )

    # ==================================================
    # GET HISTORY
    # ==================================================

    def get_history(
        self,
        db: Session,
        user_id: int,
        limit: int = 20
    ) -> List[BehavioralProfileHistory]:

        return (
            db.query(BehavioralProfileHistory)
            .filter(BehavioralProfileHistory.user_id == user_id)
            .order_by(BehavioralProfileHistory.created_at.desc())
            .limit(limit)
            .all()
        )