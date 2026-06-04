FEATURE_NAMES = [
    "sleep_hours",
    "exercise_minutes",
    "water_intake_liters",
    "stress_level",
    "screen_time_hours",
    "smoker",
    "alcohol_use",
    "diet_quality",
    "fruits_per_day",
    "vegetables_per_day"
]


def explain_prediction(importances):
    pairs = list(
        zip(FEATURE_NAMES, importances)
    )

    pairs.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return [
        {
            "feature": name,
            "impact": round(score, 4)
        }
        for name, score in pairs[:5]
    ]