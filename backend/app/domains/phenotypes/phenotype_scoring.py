from typing import Dict


class PhenotypeScoringEngine:
    """
    Rule-based scoring engine for behavioral phenotypes.
    Phase 4 foundation layer (NO ML YET).
    """

    def score(self, features: Dict[str, float]) -> Dict[str, float]:

        stress = features.get("stress_level", 0)
        sleep = features.get("sleep_hours", 0)
        screen = features.get("screen_time_hours", 0)
        exercise = features.get("exercise_minutes", 0)
        smoker = features.get("smoker", 0)
        alcohol = features.get("alcohol_use", 0)
        diet = features.get("diet_quality", 0)
        water = features.get("water_intake_liters", 0)

        return {
            "burnout": self._burnout(stress, sleep, screen),
            "overwhelmed": self._overwhelmed(stress, sleep),
            "non_adherent": self._non_adherent(smoker, alcohol, diet),
            "cardiometabolic": self._cardiometabolic(stress, exercise, diet),
            "prevention": self._prevention(stress, sleep, exercise),
        }

    # -------------------------
    # Individual scorers
    # -------------------------

    def _burnout(self, stress, sleep, screen) -> float:
        return min(
            1.0,
            (stress / 10) * 0.5 +
            (max(0, 6 - sleep) / 6) * 0.3 +
            (screen / 12) * 0.2
        )

    def _overwhelmed(self, stress, sleep) -> float:
        return min(
            1.0,
            (stress / 10) * 0.7 +
            (max(0, 6 - sleep) / 6) * 0.3
        )

    def _non_adherent(self, smoker, alcohol, diet) -> float:
        return min(
            1.0,
            (smoker * 0.4) +
            (alcohol * 0.3) +
            (max(0, 5 - diet) / 5) * 0.3
        )

    def _cardiometabolic(self, stress, exercise, diet) -> float:
        return min(
            1.0,
            (stress / 10) * 0.4 +
            (max(0, 30 - exercise) / 30) * 0.3 +
            (max(0, 5 - diet) / 5) * 0.3
        )

    def _prevention(self, stress, sleep, exercise) -> float:
        return min(
            1.0,
            1 - (
                (stress / 10) * 0.4 +
                (max(0, 6 - sleep) / 6) * 0.3 +
                (max(0, 30 - exercise) / 30) * 0.3
            )
        )