from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.prediction import Prediction
from app.models.prediction_symptom import PredictionSymptom
from app.models.health_report import HealthReport
from app.models.disease_risk_history import DiseaseRiskHistory
from app.models.lifestyle_log import LifestyleLog
from app.models.health_alert import HealthAlert

from app.schemas.assessment import HealthAssessmentRequest

from app.services.prediction_service import generate_prediction
from app.services.prediction_history_service import get_user_prediction_history
from app.services.alert_service import generate_alerts_from_prediction

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"]
)


# =====================================
# HISTORY API
# =====================================
@router.get("/history")
def get_prediction_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    predictions = get_user_prediction_history(db, current_user.id)

    return {
        "history": predictions,
        "total": len(predictions)
    }


# =====================================
# ANALYZE API (MAIN ENGINE)
# =====================================
@router.post("/analyze")
def analyze_health(
    payload: HealthAssessmentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. AI Prediction
    result = generate_prediction(payload)

    # 2. Lifestyle log
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
        risk_score=result["risk_score"]
    )
    db.add(lifestyle)
    db.flush()

    # 3. Prediction record
    prediction = Prediction(
        user_id=current_user.id,
        predicted_disease=result["predicted_disease"],
        health_score=result["health_score"],
        risk_score=result["risk_score"],
        ai_confidence=result["ai_confidence"],
        risk_level=result["risk_level"],
        urgency=result["urgency"],
        recommendation=result["recommendation"],
        explanation="\n".join(result["explanation"]),
        model_version="v1.0"
    )
    db.add(prediction)
    db.flush()

    # 4. Symptoms
    for symptom in payload.symptoms:
        db.add(PredictionSymptom(
            prediction_id=prediction.id,
            symptom=symptom
        ))

    # 5. Health report
    report = HealthReport(
        user_id=current_user.id,
        health_score=result["health_score"],
        risk_score=result["risk_score"],
        ai_confidence=result["ai_confidence"],
        predicted_disease=result["predicted_disease"],
        risk_level=result["risk_level"],
        urgency=result["urgency"],
        summary="\n".join(result["explanation"]),
        recommendations=result["recommendation"],
        report_version="v1.0"
    )
    db.add(report)

    # 6. Disease history
    history = DiseaseRiskHistory(
        user_id=current_user.id,
        disease_name=result["predicted_disease"],
        risk_score=result["risk_score"],
        risk_level=result["risk_level"],
        ai_confidence=result["ai_confidence"]
    )
    db.add(history)

    # 7. ALERT SYSTEM (SINGLE SOURCE OF TRUTH)
    alerts = generate_alerts_from_prediction(
        user_id=current_user.id,
        result=result
    )

    for alert in alerts:
        db.add(alert)

    # 8. Commit EVERYTHING
    db.commit()

    return result