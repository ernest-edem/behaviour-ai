from app.core.celery_app import celery_app


@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=5,
)
def generate_recommendations(
    self,
    prediction_result: dict,
):
    """
    Recommendation enrichment worker.

    Receives:
        prediction_result

    Returns:
        prediction_result + recommendations
    """

    try:

        risk = float(
            prediction_result.get(
                "risk_score",
                0,
            )
        )

        recommendations = []

        if risk >= 70:
            recommendations.append(
                "Immediate clinical review recommended"
            )

        if risk >= 40:
            recommendations.append(
                "Lifestyle intervention suggested"
            )

        if risk < 40:
            recommendations.append(
                "Maintain healthy lifestyle habits"
            )

        return {
            "prediction": prediction_result,
            "recommendations": recommendations,
        }

    except Exception as exc:
        raise self.retry(exc=exc)