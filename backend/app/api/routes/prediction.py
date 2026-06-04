from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database.db import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.prediction import Prediction
from app.models.prediction_symptom import PredictionSymptom
from app.models.disease_risk_history import DiseaseRiskHistory
from app.models.lifestyle_log import LifestyleLog

from app.schemas.assessment import HealthAssessmentRequest

from app.ml.observability.prediction_logger import PredictionLogger

from app.services.async_prediction_service import AsyncPredictionService
from app.services.prediction_history_service import get_user_prediction_history
from app.services.alert_service import generate_alerts_from_prediction

from app.ml.inference.prediction_orchestrator import PredictionOrchestrator
from app.services.prediction_service import generate_prediction


router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"],
)

orchestrator = PredictionOrchestrator()

DEFAULT_MODEL_VERSION = "v1.0"


# =====================================================
# HISTORY API
# =====================================================

@router.get("/history")
def get_prediction_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    predictions = get_user_prediction_history(db, current_user.id)

    return {
        "history": predictions,
        "total": len(predictions),
    }


# =====================================================
# SYNC ANALYZE
# =====================================================

@router.post("/analyze")
def analyze_health(
    payload: HealthAssessmentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    try:
        # =================================================
        # ORCHESTRATOR FIRST
        # =================================================
        try:
            result = orchestrator.predict(payload)
        except Exception:
            result = generate_prediction(payload)

        # =================================================
        # FEATURE VECTOR GUARANTEE
        # =================================================
        feature_vector = result.get("feature_vector", {})
        if not isinstance(feature_vector, dict):
            feature_vector = {}
        result["feature_vector"] = feature_vector

        # =================================================
        # NORMALIZATION
        # =================================================
        predicted_disease = result.get("predicted_disease", "")
        predicted_condition = result.get("predicted_condition", predicted_disease)

        ai_confidence = float(result.get("ai_confidence", 0))
        confidence_score = float(result.get("confidence_score", ai_confidence))

        model_version = result.get("model_version", DEFAULT_MODEL_VERSION)

        explanations = result.get("explanation", result.get("explanations", []))
        if explanations is None:
            explanations = []

        recommendation = result.get("recommendation") or ""
        if isinstance(recommendation, list):
            recommendation = " ".join(str(x) for x in recommendation)

        # =================================================
        # LIFESTYLE LOG
        # =================================================
        lifestyle = LifestyleLog(
            user_id=current_user.id,
            sleep_hours=payload.sleep_hours,
            exercise_minutes=payload.exercise_minutes,
            water_intake_liters=payload.water_intake_liters,
            stress_level=payload.stress_level,
            screen_time_hours=payload.screen_time_hours,
            smoker=payload.smoker,
            alcohol_use=payload.alcohol_use,
            diet_quality=payload.diet_quality,
            fruits_per_day=payload.fruits_per_day,
            vegetables_per_day=payload.vegetables_per_day,
            lifestyle_score=result["health_score"],
            risk_score=result["risk_score"],
        )

        db.add(lifestyle)

        # =================================================
        # PREDICTION RECORD
        # =================================================
        prediction = Prediction(
            user_id=current_user.id,
            predicted_condition=predicted_condition,
            confidence_score=confidence_score,

            predicted_disease=predicted_disease,
            ai_confidence=ai_confidence,

            health_score=result["health_score"],
            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            urgency=result["urgency"],

            behavioral_phenotype=result.get("behavioral_phenotype"),

            recommendation=recommendation,
            explanation="\n".join(explanations),

            disease_probabilities=result.get("disease_probabilities"),
            shap_values=result.get("shap_values"),
            feature_contributions=result.get("feature_contributions"),

            prediction_source=result.get("prediction_source", "rule_engine"),

            model_name=result.get("model_name"),
            model_type=result.get("model_type"),
            model_version=model_version,
        )

        db.add(prediction)
        db.flush()

        # =================================================
        # SYMPTOMS
        # =================================================
        for symptom in payload.symptoms:
            db.add(
                PredictionSymptom(
                    prediction_id=prediction.id,
                    symptom=symptom,
                )
            )

        # =================================================
        # DISEASE HISTORY
        # =================================================
        db.add(
            DiseaseRiskHistory(
                user_id=current_user.id,
                disease_name=predicted_disease,
                risk_score=result["risk_score"],
                risk_level=result["risk_level"],
                ai_confidence=ai_confidence,
            )
        )

        # =================================================
        # ALERTS
        # =================================================
        alerts = generate_alerts_from_prediction(
            user_id=current_user.id,
            result=result,
        )

        for alert in alerts:
            db.add(alert)

        # =================================================
        # COMMIT
        # =================================================
        db.commit()

        # =================================================
        # AUDIT LOG (FIXED & SINGLE SOURCE OF TRUTH)
        # =================================================
        audit_record = PredictionLogger.log(
            user_id=current_user.id,
            input_data=payload.dict(),
            feature_vector=feature_vector,
            result=result,
            model_version=model_version,
            prediction_source=result.get("prediction_source", "rule_engine"),
        )

        print("[ML_AUDIT]", audit_record)

        db.refresh(prediction)

        return {
            **result,
            "prediction_id": prediction.id,
            "model_version": model_version,
            "mode": "sync",
        }

    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(exc)}",
        )

    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(exc)}",
        )


# =====================================================
# ASYNC ANALYZE
# =====================================================

@router.post("/analyze-async")
def analyze_health_async(
    payload: HealthAssessmentRequest,
    current_user: User = Depends(get_current_user),
):

    task = AsyncPredictionService.trigger_full_pipeline(
        payload.dict(),
        current_user.id,
    )

    return {
        "message": "Prediction queued",
        "task": task,
        "mode": "async",
    }