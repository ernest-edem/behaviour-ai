from app.models.health_alert import HealthAlert


def generate_alerts_from_prediction(
    user_id: int,
    result: dict
):
    alerts = []

    risk = result["risk_score"]
    health = result["health_score"]
    disease = result["predicted_disease"]

    # =====================
    # CRITICAL RISK
    # =====================

    if risk >= 80:
        alerts.append(
            HealthAlert(
                user_id=user_id,
                alert_type="critical",
                title="Critical Health Risk Detected",
                message="Immediate medical attention recommended",
                risk_score=risk,
                health_score=health,
                severity="high",
            )
        )

    # =====================
    # LOW HEALTH SCORE
    # =====================

    if health < 40:
        alerts.append(
            HealthAlert(
                user_id=user_id,
                alert_type="warning",
                title="Low Health Score",
                message="Health indicators are below safe range",
                risk_score=risk,
                health_score=health,
                severity="medium",
            )
        )

    # =====================
    # HIGH-RISK DISEASES
    # =====================

    if disease in [
        "Diabetes",
        "Cardiovascular",
        "Hypertension",
    ]:
        alerts.append(
            HealthAlert(
                user_id=user_id,
                alert_type="critical",
                title=f"{disease} Risk Detected",
                message="High probability of serious condition detected",
                risk_score=risk,
                health_score=health,
                severity="high",
            )
        )

    return alerts