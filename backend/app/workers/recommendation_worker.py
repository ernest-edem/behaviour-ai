from app.core.celery_app import celery_app


@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=5,
)
def generate_recommendations(self, prediction_result: dict):
    try:
        # lightweight rule-based expansion for now
        risk = prediction_result.get("risk_score", 0)

        recommendations = []

        if risk > 70:
            recommendations.append("Immediate clinical review recommended")

        if risk > 40:
            recommendations.append("Lifestyle intervention suggested")

        return {
            "recommendations": recommendations
        }

    except Exception as exc:
        raise self.retry(exc=exc)