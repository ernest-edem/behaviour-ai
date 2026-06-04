from app.core.celery_app import celery_app


@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=5,
)
def generate_report(self, user_id: int, prediction: dict):
    try:
        return {
            "user_id": user_id,
            "report": {
                "summary": prediction.get("predicted_disease"),
                "risk": prediction.get("risk_score"),
                "status": "generated"
            }
        }

    except Exception as exc:
        raise self.retry(exc=exc)