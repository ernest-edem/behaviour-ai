from fastapi import APIRouter
from app.workers.prediction_worker import run_prediction

router = APIRouter(prefix="/async-predictions", tags=["Async Prediction"])


@router.post("/analyze")
def async_analyze(payload: dict):
    task = run_prediction.delay(payload)

    return {
        "task_id": task.id,
        "status": "queued"
    }