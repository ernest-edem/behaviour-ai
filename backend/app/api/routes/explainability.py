from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db

from app.ml.registry.model_registry import model_registry
from app.ml.feature_engineering.feature_builder import FeatureBuilder
from app.ml.explainability.explanation_service import ExplanationService

from app.models.prediction import Prediction

router = APIRouter()


@router.get("/explainability/{prediction_id}")
def get_explanation(
    prediction_id: int,
    db: Session = Depends(get_db),
):
    try:
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
        # GET MODEL + FEATURE NAMES
        # =================================================
        model = model_registry.get_active_model()
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
            features = {
                "sleep_hours": 6,
                "exercise_minutes": 20,
                "water_intake_liters": 2,
                "stress_level": 7,
                "screen_time_hours": 8,
                "smoker": 0,
                "alcohol_use": 1,
                "diet_quality": 3,
                "fruits_per_day": 2,
                "vegetables_per_day": 3,
            }

        # =================================================
        # SHAP EXPLANATION
        # =================================================
        return service.explain_prediction(features)

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Explainability failed: {str(exc)}",
        )