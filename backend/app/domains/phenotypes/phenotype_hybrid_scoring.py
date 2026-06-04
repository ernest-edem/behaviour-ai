from typing import Dict


class PhenotypeHybridScoringEngine:
    """
    Phase 4 Step C:
    Hybrid scoring system (Rule + Weighted Intelligence Layer)

    NOT SHAP.
    Prepares system for explainability.
    """

    def __init__(self, weights: Dict[str, float] | None = None):
        # Default behavioral importance weights
        self.weights = weights or {
            "stress_level": 0.25,
            "sleep_hours": 0.20,
            "screen_time_hours": 0.15,
            "exercise_minutes": 0.15,
            "diet_quality": 0.10,
            "smoker": 0.10,
            "alcohol_use": 0.05
        }

    def score(self, features: Dict[str, float]) -> Dict[str, float]:

        # Normalize inputs
        stress = features.get("stress_level", 0) / 10
        sleep = max(0, 6 - features.get("sleep_hours", 0)) / 6
        screen = features.get("screen_time_hours", 0) / 12
        exercise = max(0, 30 - features.get("exercise_minutes", 0)) / 30
        diet = max(0, 5 - features.get("diet_quality", 0)) / 5
        smoker = float(features.get("smoker", 0))
        alcohol = float(features.get("alcohol_use", 0))

        weighted_risk = (
            stress * self.weights["stress_level"] +
            sleep * self.weights["sleep_hours"] +
            screen * self.weights["screen_time_hours"] +
            exercise * self.weights["exercise_minutes"] +
            diet * self.weights["diet_quality"] +
            smoker * self.weights["smoker"] +
            alcohol * self.weights["alcohol_use"]
        )

        # Derived phenotype signals (normalized 0–1)
        return {
            "overall_risk": min(1.0, weighted_risk),

            "stress_signal": stress,
            "sleep_deficit_signal": sleep,
            "screen_overuse_signal": screen,
            "exercise_deficit_signal": exercise,
            "diet_risk_signal": diet,

            # Explainability bridge (PRE-SHAP)
            "feature_contributions": {
                "stress_level": stress * self.weights["stress_level"],
                "sleep_hours": sleep * self.weights["sleep_hours"],
                "screen_time": screen * self.weights["screen_time_hours"],
                "exercise_minutes": exercise * self.weights["exercise_minutes"],
                "diet_quality": diet * self.weights["diet_quality"],
                "smoker": smoker * self.weights["smoker"],
                "alcohol_use": alcohol * self.weights["alcohol_use"],
            }
        }