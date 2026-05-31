def generate_recommendations(data):
    recommendations = []

    if data.sleep_hours < 6:
        recommendations.append(
            "Increase sleep duration to 7-9 hours daily."
        )

    if data.exercise_minutes < 30:
        recommendations.append(
            "Increase physical activity."
        )

    if data.stress_level > 7:
        recommendations.append(
            "Practice stress reduction techniques."
        )

    if data.smoker:
        recommendations.append(
            "Consider smoking cessation support."
        )

    if data.alcohol_use:
        recommendations.append(
            "Reduce alcohol consumption."
        )

    if data.diet_quality < 5:
        recommendations.append(
            "Improve nutrition quality."
        )

    if not recommendations:
        recommendations.append(
            "Maintain current healthy lifestyle habits."
        )

    return recommendations