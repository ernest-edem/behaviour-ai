from typing import Dict


def generate_prediction(data):
    """
    BehaviorLens AI Rule-Based Prediction Engine

    This serves as:
    - Baseline prediction engine
    - Fallback engine when ML model unavailable
    - Explainability layer
    """

    risk_score = 0
    explanations = []

    # =====================================
    # DISEASE SCORES
    # =====================================

    disease_scores = {
        "Diabetes": 0,
        "Hypertension": 0,
        "Obesity": 0,
        "Cardiovascular Disease": 0,
        "Stress Related Disorder": 0,
        "Sleep Disorder": 0,
        "General Health Risk": 0
    }

    # =====================================
    # SLEEP ANALYSIS
    # =====================================

    if getattr(data, "sleep_hours", None) is not None:

        if data.sleep_hours < 5:
            risk_score += 20

            disease_scores["Sleep Disorder"] += 40
            disease_scores["Hypertension"] += 10

            explanations.append(
                "Poor sleep significantly increased health risk."
            )

        elif data.sleep_hours < 7:
            risk_score += 10

    # =====================================
    # STRESS ANALYSIS
    # =====================================

    if getattr(data, "stress_level", None) is not None:

        if data.stress_level >= 8:
            risk_score += 20

            disease_scores["Stress Related Disorder"] += 40
            disease_scores["Hypertension"] += 15
            disease_scores["Cardiovascular Disease"] += 10

            explanations.append(
                "High stress significantly increased disease risk."
            )

        elif data.stress_level >= 6:
            risk_score += 10

    # =====================================
    # PHYSICAL ACTIVITY
    # =====================================

    if getattr(data, "exercise_minutes", None) is not None:

        if data.exercise_minutes < 30:
            risk_score += 15

            disease_scores["Obesity"] += 20
            disease_scores["Cardiovascular Disease"] += 20

            explanations.append(
                "Low physical activity contributed to risk."
            )

    # =====================================
    # BMI ANALYSIS
    # =====================================

    if getattr(data, "bmi", None) is not None:

        if data.bmi >= 30:
            risk_score += 20

            disease_scores["Obesity"] += 40
            disease_scores["Diabetes"] += 20
            disease_scores["Hypertension"] += 20

            explanations.append(
                "Obesity indicators increased disease risk."
            )

        elif data.bmi >= 25:
            risk_score += 10

    # =====================================
    # SMOKING
    # =====================================

    if getattr(data, "smoker", False):

        risk_score += 20

        disease_scores["Cardiovascular Disease"] += 30
        disease_scores["Hypertension"] += 15

        explanations.append(
            "Smoking behavior increased cardiovascular risk."
        )

    # =====================================
    # ALCOHOL
    # =====================================

    if getattr(data, "alcohol_use", False):

        risk_score += 10

        disease_scores["Hypertension"] += 10

        explanations.append(
            "Alcohol use contributed to health risk."
        )

    # =====================================
    # DIET QUALITY
    # =====================================

    if getattr(data, "diet_quality", None) is not None:

        if data.diet_quality < 5:
            risk_score += 15

            disease_scores["Diabetes"] += 15
            disease_scores["Obesity"] += 15

            explanations.append(
                "Poor diet quality increased disease risk."
            )

    # =====================================
    # HYDRATION
    # =====================================

    if getattr(data, "water_intake_liters", None) is not None:

        if data.water_intake_liters < 1.5:
            risk_score += 5

            explanations.append(
                "Low hydration may negatively affect health."
            )

    # =====================================
    # SCREEN TIME
    # =====================================

    if getattr(data, "screen_time_hours", None) is not None:

        if data.screen_time_hours > 8:
            risk_score += 10

            disease_scores["Stress Related Disorder"] += 10

            explanations.append(
                "Excessive screen time may impact wellbeing."
            )

    # =====================================
    # AGE FACTOR
    # =====================================

    if getattr(data, "age", None) is not None:

        if data.age >= 60:
            risk_score += 10

            disease_scores["Hypertension"] += 10
            disease_scores["Cardiovascular Disease"] += 10

    # =====================================
    # SYMPTOM ANALYSIS
    # =====================================

    symptoms = getattr(data, "symptoms", [])

    symptoms_text = " ".join(
        symptom.lower()
        for symptom in symptoms
    )

    # Diabetes

    if (
        "frequent urination" in symptoms_text
        or "excessive thirst" in symptoms_text
    ):
        disease_scores["Diabetes"] += 35

    # Cardiovascular

    if (
        "chest pain" in symptoms_text
        or "shortness of breath" in symptoms_text
    ):
        disease_scores["Cardiovascular Disease"] += 40

    # Stress

    if (
        "fatigue" in symptoms_text
        and getattr(data, "stress_level", 0) >= 8
    ):
        disease_scores["Stress Related Disorder"] += 30

    # Sleep

    if (
        "insomnia" in symptoms_text
        or "daytime sleepiness" in symptoms_text
    ):
        disease_scores["Sleep Disorder"] += 30

    # =====================================
    # FINAL SCORE CALCULATION
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

    highest_score = max(
        disease_scores.values()
    )

    ai_confidence = min(
        95,
        max(60, highest_score)
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
        getattr(data, "stress_level", 0) >= 8
    ):
        phenotype = (
            "Emotionally Overwhelmed Profile"
        )

    if (
        getattr(data, "exercise_minutes", 100) < 20
        and getattr(data, "bmi", 0) >= 25
    ):
        phenotype = (
            "High Cardiometabolic Risk Profile"
        )

    # =====================================
    # NORMALIZED PROBABILITIES
    # =====================================

    total = sum(disease_scores.values())

    if total > 0:

        disease_probabilities = {
            disease: round(
                (score / total) * 100,
                2
            )
            for disease, score in disease_scores.items()
        }

    else:

        disease_probabilities = {
            disease: 0
            for disease in disease_scores
        }

    # =====================================
    # RECOMMENDATION ENGINE
    # =====================================

    recommendation = (
        "Improve sleep quality, increase physical activity, "
        "maintain a healthy diet, reduce stress levels, "
        "avoid smoking, limit alcohol consumption, "
        "and seek professional medical evaluation if symptoms persist."
    )

    # =====================================
    # RETURN RESULT
    # =====================================

    return {
        "health_score": round(
            health_score,
            2
        ),
        "risk_score": round(
            risk_score,
            2
        ),
        "ai_confidence": round(
            ai_confidence,
            2
        ),
        "predicted_disease": predicted_disease,
        "risk_level": risk_level,
        "urgency": (
            "High"
            if risk_level in ["High", "Critical"]
            else "Low"
        ),
        "behavioral_phenotype": phenotype,
        "disease_probabilities": disease_probabilities,
        "explanation": explanations,
        "recommendation": recommendation
    }