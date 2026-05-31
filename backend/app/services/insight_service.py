from sqlalchemy.orm import Session
from app.models.prediction import Prediction


def generate_health_insights(predictions: list) -> list:

    if not predictions:
        return ["No data available to generate insights."]

    insights = []

    latest = predictions[-1]
    first = predictions[0]

    # -----------------------------
    # TREND ANALYSIS
    # -----------------------------
    if latest.risk_score > first.risk_score:
        insights.append(
            "Your health risk is increasing over time. Lifestyle factors need attention."
        )
    elif latest.risk_score < first.risk_score:
        insights.append(
            "Your health risk is improving. Keep maintaining your current habits."
        )
    else:
        insights.append(
            "Your health risk is stable."
        )

    # -----------------------------
    # HEALTH SCORE INSIGHT
    # -----------------------------
    if latest.health_score < 40:
        insights.append(
            "Your overall health score is low, indicating multiple risk factors."
        )
    elif latest.health_score > 70:
        insights.append(
            "Your health score is strong, indicating healthy lifestyle patterns."
        )

    # -----------------------------
    # RISK DRIVER ANALYSIS (SIMPLIFIED)
    # -----------------------------
    stress_high = any(p.risk_score > 70 for p in predictions)
    sleep_issue = any("sleep" in (p.explanation or "").lower() for p in predictions)
    lifestyle_risk = any(p.risk_level == "High" for p in predictions)

    if stress_high:
        insights.append(
            "High stress episodes are significantly contributing to your risk levels."
        )

    if sleep_issue:
        insights.append(
            "Poor sleep patterns are negatively affecting your health trends."
        )

    if lifestyle_risk:
        insights.append(
            "Repeated high-risk assessments indicate persistent lifestyle concerns."
        )

    # -----------------------------
    # MOST IMPORTANT SUMMARY
    # -----------------------------
    insights.append(
        f"Latest assessment shows {latest.predicted_disease} as primary concern with {latest.risk_level} risk level."
    )

    return insights