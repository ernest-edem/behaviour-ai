from app.workers.prediction_worker import run_prediction
from app.workers.recommendation_worker import generate_recommendations
from app.workers.report_worker import generate_report


class AsyncPredictionService:

    @staticmethod
    def trigger_full_pipeline(payload: dict, user_id: int):

        prediction_task = run_prediction.delay(payload)

        return {
            "prediction_task_id": prediction_task.id,
            "status": "queued",
        }