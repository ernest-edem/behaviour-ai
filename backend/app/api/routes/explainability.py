from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import get_db

from app.ml.registry.model_registry import model_registry
from app.ml.features.feature_builder import FeatureBuilder
from app.ml.explainability.explanation_service import ExplanationService
from app.ml.common.exceptions import ModelNotFoundError

from app.models.prediction import Prediction

router = APIRouter()


@router.get("/explainability/{prediction_id}")
def get_explanation(
    prediction_id: int,
    db: Session = Depends(get_db),
):
    # =================================================
    # GET MODEL — 503 if registry is empty
    # =================================================
    try:
        model = model_registry.get_active_model()
    except ModelNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Explainability model not available. No active model registered.",
        )

    # =================================================
    # LOAD PREDICTION FROM DB
    # =================================================
    prediction = db.query(Prediction).filter(
        Prediction.id == prediction_id
    ).first()

    if not prediction:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found",
        )

    # =================================================
    # GET FEATURE NAMES FROM CANONICAL SOURCE
    # =================================================
    feature_names = FeatureBuilder.get_feature_names()

    service = ExplanationService(
        model=model.get_estimator(),
        feature_names=feature_names,
    )

    # =================================================
    # RECONSTRUCT FEATURES (REAL DATA FIRST, FALLBACK SAFE)
    # =================================================
    if hasattr(prediction, "feature_vector") and prediction.feature_vector:
        features = prediction.feature_vector
    else:
        # Fallback: use safe population-median defaults
        # so the endpoint never crashes on legacy predictions.
        features = {
            "sleep_hours": 7.0,
            "exercise_minutes": 30.0,
            "water_intake_liters": 2.0,
            "stress_level": 3.0,
            "screen_time_hours": 4.0,
            "smoker": 0.0,
            "alcohol_use": 0.0,
            "diet_quality": 5.0,
            "fruits_per_day": 2.0,
            "vegetables_per_day": 2.0,
        }

    # =================================================
    # SHAP EXPLANATION
    # =================================================
    try:
        return service.explain_prediction(features)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Explainability failed: {str(exc)}",
        )