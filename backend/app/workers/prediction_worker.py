from app.core.celery_app import celery_app
from app.ml.inference.prediction_orchestrator import PredictionOrchestrator


@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=5,
)
def run_prediction(self, payload: dict):
    try:
        orchestrator = PredictionOrchestrator()
        return orchestrator.predict(payload)

    except Exception as exc:
        raise self.retry(exc=exc)