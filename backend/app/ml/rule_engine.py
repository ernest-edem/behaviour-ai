from typing import Dict


def generate_prediction(data):
    risk_score = 0
    explanations = []

    disease_scores = {
        "Diabetes": 0,
        "Hypertension": 0,
        "Obesity": 0,
        "Cardiovascular Disease": 0,
        "Stress Related Disorder": 0,
        "Sleep Disorder": 0,
    }

    # =====================================
    # SLEEP
    # =====================================

    if data.sleep_hours is not None:

        if data.sleep_hours < 5:
            risk_score += 20
            disease_scores["Sleep Disorder"] += 35
            disease_scores["Hypertension"] += 10

            explanations.append(
                "Poor sleep significantly increased health risk."
            )

        elif data.sleep_hours < 7:
            risk_score += 10

    # =====================================
    # STRESS
    # =====================================

    if data.stress_level is not None:

        if data.stress_level >= 8:
            risk_score += 20

            disease_scores["Stress Related Disorder"] += 40
            disease_scores["Hypertension"] += 15
            disease_scores["Cardiovascular Disease"] += 10

            explanations.append(
                "Very high stress increased behavioral risk."
            )

        elif data.stress_level >= 6:
            risk_score += 10

    # =====================================
    # EXERCISE
    # =====================================

    if data.exercise_minutes is not None:

        if data.exercise_minutes < 30:
            risk_score += 15

            disease_scores["Obesity"] += 20
            disease_scores["Cardiovascular Disease"] += 20

            explanations.append(
                "Physical inactivity contributed to risk."
            )

    # =====================================
    # BMI
    # =====================================

    if getattr(data, "bmi", None):

        if data.bmi >= 30:
            risk_score += 20

            disease_scores["Obesity"] += 40
            disease_scores["Diabetes"] += 20
            disease_scores["Hypertension"] += 20

            explanations.append(
                "Obesity-related indicators increased risk."
            )

        elif data.bmi >= 25:
            risk_score += 10

    # =====================================
    # SMOKING
    # =====================================

    if data.smoker:

        risk_score += 20

        disease_scores["Cardiovascular Disease"] += 30
        disease_scores["Hypertension"] += 15

        explanations.append(
            "Smoking behavior increased cardiovascular risk."
        )

    # =====================================
    # ALCOHOL
    # =====================================

    if data.alcohol_use:

        risk_score += 10

        disease_scores["Hypertension"] += 10

        explanations.append(
            "Alcohol consumption contributed to risk."
        )

    # =====================================
    # DIET QUALITY
    # =====================================

    if data.diet_quality is not None:

        if data.diet_quality < 5:
            risk_score += 15

            disease_scores["Obesity"] += 15
            disease_scores["Diabetes"] += 15

            explanations.append(
                "Poor dietary quality increased risk."
            )

    # =====================================
    # SCREEN TIME
    # =====================================

    if getattr(data, "screen_time_hours", None):

        if data.screen_time_hours > 8:
            risk_score += 10

            disease_scores["Stress Related Disorder"] += 10

            explanations.append(
                "Excessive screen time may affect wellbeing."
            )

    # =====================================
    # HYDRATION
    # =====================================

    if getattr(data, "water_intake_liters", None):

        if data.water_intake_liters < 1.5:
            risk_score += 5

            explanations.append(
                "Low hydration may affect overall health."
            )

    # =====================================
    # SYMPTOMS
    # =====================================

    symptoms_text = " ".join(
        symptom.lower()
        for symptom in data.symptoms
    )

    if "frequent urination" in symptoms_text:
        disease_scores["Diabetes"] += 30

    if "excessive thirst" in symptoms_text:
        disease_scores["Diabetes"] += 30

    if "chest pain" in symptoms_text:
        disease_scores["Cardiovascular Disease"] += 40

    if "shortness of breath" in symptoms_text:
        disease_scores["Cardiovascular Disease"] += 35

    if "fatigue" in symptoms_text:
        disease_scores["Stress Related Disorder"] += 15

    # =====================================
    # FINAL SCORES
    # =====================================

    risk_score = min(risk_score, 100)

    health_score = max(
        0,
        100 - risk_score
    )

    predicted_disease = max(
        disease_scores,
        key=disease_scores.get
    )

    ai_confidence = min(
        95,
        max(disease_scores.values())
    )

    # =====================================
    # RISK LEVEL
    # =====================================

    if risk_score < 20:
        risk_level = "Low"

    elif risk_score < 40:
        risk_level = "Mild"

    elif risk_score < 60:
        risk_level = "Moderate"

    elif risk_score < 80:
        risk_level = "High"

    else:
        risk_level = "Critical"

    # =====================================
    # BEHAVIORAL PHENOTYPE
    # =====================================

    phenotype = "Prevention Opportunity Profile"

    if (
        data.stress_level is not None
        and data.stress_level >= 8
    ):
        phenotype = "Emotionally Overwhelmed Profile"

    if (
        data.exercise_minutes is not None
        and data.exercise_minutes < 20
    ):
        phenotype = "High Cardiometabolic Risk Profile"

    # =====================================
    # RECOMMENDATIONS
    # =====================================

    recommendation = (
        "Increase physical activity, improve sleep quality, "
        "reduce stress levels, maintain a healthy diet, "
        "and seek medical evaluation if symptoms persist."
    )

    return {
        "health_score": round(health_score, 2),
        "risk_score": round(risk_score, 2),
        "ai_confidence": round(ai_confidence, 2),
        "predicted_disease": predicted_disease,
        "risk_level": risk_level,
        "urgency": (
            "High"
            if risk_level in ["High", "Critical"]
            else "Low"
        ),
        "behavioral_phenotype": phenotype,
        "disease_probabilities": disease_scores,
        "explanation": explanations,
        "recommendation": recommendation,
    }