from typing import Dict


def generate_prediction(data):
    """
    BehaviorLens AI Rule-Based Prediction Engine

    This serves as:
    - Baseline prediction engine
    - Fallback engine when ML model unavailable
    - Explainability layer
    """

    raw_risk_score = 0
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
            raw_risk_score += 20

            disease_scores["Sleep Disorder"] += 40
            disease_scores["Hypertension"] += 10

            explanations.append(
                "Poor sleep significantly increased health risk."
            )

        elif data.sleep_hours < 7:
            raw_risk_score += 10

    # =====================================
    # STRESS ANALYSIS
    # =====================================

    if getattr(data, "stress_level", None) is not None:

        if data.stress_level >= 8:
            raw_risk_score += 20

            disease_scores["Stress Related Disorder"] += 40
            disease_scores["Hypertension"] += 15
            disease_scores["Cardiovascular Disease"] += 10

            explanations.append(
                "High stress significantly increased disease risk."
            )

        elif data.stress_level >= 6:
            raw_risk_score += 10

    # =====================================
    # PHYSICAL ACTIVITY
    # =====================================

    if getattr(data, "exercise_minutes", None) is not None:

        if data.exercise_minutes < 30:
            raw_risk_score += 15

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
            raw_risk_score += 20

            disease_scores["Obesity"] += 40
            disease_scores["Diabetes"] += 20
            disease_scores["Hypertension"] += 20

            explanations.append(
                "Obesity indicators increased disease risk."
            )

        elif data.bmi >= 25:
            raw_risk_score += 10

    # =====================================
    # SMOKING
    # =====================================

    if getattr(data, "smoker", False):

        raw_risk_score += 20

        disease_scores["Cardiovascular Disease"] += 30
        disease_scores["Hypertension"] += 15

        explanations.append(
            "Smoking behavior increased cardiovascular risk."
        )

    # =====================================
    # ALCOHOL
    # =====================================

    if getattr(data, "alcohol_use", False):

        raw_risk_score += 10

        disease_scores["Hypertension"] += 10

        explanations.append(
            "Alcohol use contributed to health risk."
        )

    # =====================================
    # DIET QUALITY
    # =====================================

    if getattr(data, "diet_quality", None) is not None:

        if data.diet_quality < 5:
            raw_risk_score += 15

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
            raw_risk_score += 5

            explanations.append(
                "Low hydration may negatively affect health."
            )

    # =====================================
    # SCREEN TIME
    # =====================================

    if getattr(data, "screen_time_hours", None) is not None:

        if data.screen_time_hours > 8:
            raw_risk_score += 10

            disease_scores["Stress Related Disorder"] += 10

            explanations.append(
                "Excessive screen time may impact wellbeing."
            )

    # =====================================
    # AGE FACTOR
    # =====================================

    if getattr(data, "age", None) is not None:

        if data.age >= 60:
            raw_risk_score += 10

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

    if (
        "frequent urination" in symptoms_text
        or "excessive thirst" in symptoms_text
    ):
        disease_scores["Diabetes"] += 35

    if (
        "chest pain" in symptoms_text
        or "shortness of breath" in symptoms_text
    ):
        disease_scores["Cardiovascular Disease"] += 40

    if (
        "fatigue" in symptoms_text
        and getattr(data, "stress_level", 0) >= 8
    ):
        disease_scores["Stress Related Disorder"] += 30

    if (
        "insomnia" in symptoms_text
        or "daytime sleepiness" in symptoms_text
    ):
        disease_scores["Sleep Disorder"] += 30

    # =====================================
    # SCORE NORMALIZATION
    # =====================================

    MAX_RAW_RISK = 135

    risk_score = round(
        (raw_risk_score / MAX_RAW_RISK) * 100,
        2
    )

    risk_score = min(
        95,
        max(5, risk_score)
    )

    health_score = round(
        100 - risk_score,
        2
    )

    # =====================================
    # PREDICTION
    # =====================================

    predicted_disease = max(
        disease_scores,
        key=disease_scores.get
    )

    # =====================================
    # NORMALIZED PROBABILITIES
    # =====================================

    total_score = sum(
        disease_scores.values()
    )

    if total_score > 0:

        disease_probabilities = {
            disease: round(
                (score / total_score) * 100,
                2
            )
            for disease, score in disease_scores.items()
        }

        highest_score = max(
            disease_scores.values()
        )

        ai_confidence = round(
            min(
                95,
                50 + (
                    highest_score / total_score
                ) * 50
            ),
            2
        )

    else:

        disease_probabilities = {
            disease: 0
            for disease in disease_scores
        }

        ai_confidence = 50

    # =====================================
    # RISK LEVEL
    # =====================================

    if risk_score < 25:
        risk_level = "Low"

    elif risk_score < 45:
        risk_level = "Mild"

    elif risk_score < 65:
        risk_level = "Moderate"

    elif risk_score < 85:
        risk_level = "High"

    else:
        risk_level = "Critical"

    # =====================================
    # BEHAVIORAL PHENOTYPE
    # =====================================

    phenotype = "Prevention Opportunity Profile"

    if getattr(data, "stress_level", 0) >= 8:
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
    # PERSONALIZED RECOMMENDATIONS
    # =====================================

    recommendations = []

    if getattr(data, "sleep_hours", 8) < 6:
        recommendations.append(
            "Improve sleep duration and quality."
        )

    if getattr(data, "stress_level", 0) >= 7:
        recommendations.append(
            "Practice stress management techniques."
        )

    if getattr(data, "exercise_minutes", 100) < 30:
        recommendations.append(
            "Increase daily physical activity."
        )

    if getattr(data, "diet_quality", 10) < 5:
        recommendations.append(
            "Adopt a healthier and more balanced diet."
        )

    if getattr(data, "smoker", False):
        recommendations.append(
            "Consider smoking cessation support."
        )

    if getattr(data, "alcohol_use", False):
        recommendations.append(
            "Reduce alcohol consumption."
        )

    if getattr(data, "water_intake_liters", 3) < 1.5:
        recommendations.append(
            "Increase daily water intake."
        )

    if not recommendations:
        recommendations.append(
            "Maintain current healthy lifestyle habits."
        )

    recommendation = " ".join(recommendations)

    # =====================================
    # RETURN RESULT
    # =====================================

    return {
        "health_score": health_score,
        "risk_score": risk_score,
        "ai_confidence": ai_confidence,
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