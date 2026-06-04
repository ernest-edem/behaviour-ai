from typing import Any, Dict

import pandas as pd

from app.ml.common.exceptions import (
    FeatureEngineeringError,
)


FEATURE_COLUMNS = [
    "sleep_hours",
    "exercise_minutes",
    "water_intake_liters",
    "stress_level",
    "screen_time_hours",
    "smoker",
    "alcohol_use",
    "diet_quality",
    "fruits_per_day",
    "vegetables_per_day",
]


class FeatureBuilder:
    """
    Produces named features suitable for:

    - Scikit-learn
    - Random Forest
    - XGBoost
    - SHAP

    Feature names are preserved to support explainability.
    """

    @staticmethod
    def build(data: Any) -> Dict[str, float]:
        try:
            features = {
                "sleep_hours": float(data.sleep_hours),
                "exercise_minutes": float(data.exercise_minutes),
                "water_intake_liters": float(data.water_intake_liters),
                "stress_level": float(data.stress_level),
                "screen_time_hours": float(data.screen_time_hours),
                "smoker": float(int(data.smoker)),
                "alcohol_use": float(int(data.alcohol_use)),
                "diet_quality": float(data.diet_quality),
                "fruits_per_day": float(data.fruits_per_day),
                "vegetables_per_day": float(data.vegetables_per_day),
            }

            return features

        except AttributeError as exc:
            raise FeatureEngineeringError(
                f"Missing required feature: {exc}"
            ) from exc

        except Exception as exc:
            raise FeatureEngineeringError(
                f"Feature building failed: {exc}"
            ) from exc

    @staticmethod
    def to_dataframe(
        features: Dict[str, float]
    ) -> pd.DataFrame:
        return pd.DataFrame(
            [features],
            columns=FEATURE_COLUMNS,
        )

    @staticmethod
    def get_feature_names() -> list[str]:
        return FEATURE_COLUMNS.copy()