from app.core.celery_app import celery_app


@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=5,
)
def generate_report(
    self,
    workflow_result: dict,
):
    """
    Final reporting worker.

    Receives:
        {
            "user_id": int,
            "prediction": {...},
            "recommendations": [...]
        }

    Returns:
        Enterprise-friendly report payload.
    """

    try:

        prediction = workflow_result.get(
            "prediction",
            {},
        )

        recommendations = workflow_result.get(
            "recommendations",
            [],
        )

        user_id = workflow_result.get(
            "user_id",
        )

        report = {
            "summary": prediction.get(
                "predicted_disease"
            ),
            "risk_score": prediction.get(
                "risk_score"
            ),
            "risk_level": prediction.get(
                "risk_level"
            ),
            "health_score": prediction.get(
                "health_score"
            ),
            "confidence": prediction.get(
                "ai_confidence"
            ),
            "behavioral_phenotype": prediction.get(
                "behavioral_phenotype"
            ),
            "recommendations": recommendations,
            "status": "generated",
        }

        return {
            "user_id": user_id,
            "prediction": prediction,
            "report": report,
        }

    except Exception as exc:
        raise self.retry(exc=exc)