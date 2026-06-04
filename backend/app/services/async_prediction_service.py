from app.workers.prediction_worker import run_prediction


class AsyncPredictionService:
    """
    Async orchestration entrypoint.

    Current architecture:
        FastAPI
            ↓
        Prediction Worker

    Future architecture:
        Prediction Worker
            ↓
        Recommendation Worker
            ↓
        Report Worker
    """

    @staticmethod
    def trigger_full_pipeline(
        payload: dict,
        user_id: int,
    ):
        prediction_task = run_prediction.delay(payload)

        return {
            "user_id": user_id,
            "prediction_task_id": prediction_task.id,
            "status": "queued",
            "pipeline": "prediction",
        }