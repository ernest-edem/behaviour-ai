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
    Canonical feature engineering layer.

    Responsibilities:
    - Build model-ready feature vectors
    - Maintain schema stability
    - Support Pydantic objects and dict payloads
    - Preserve feature ordering for training parity
    - Support SHAP explainability
    """

    # ==================================================
    # MAIN FEATURE EXTRACTION
    # ==================================================

    @staticmethod
    def build(
        data: Any,
    ) -> Dict[str, float]:

        try:

            features = {
                "sleep_hours": FeatureBuilder._float(
                    FeatureBuilder._get(data, "sleep_hours")
                ),
                "exercise_minutes": FeatureBuilder._float(
                    FeatureBuilder._get(data, "exercise_minutes")
                ),
                "water_intake_liters": FeatureBuilder._float(
                    FeatureBuilder._get(data, "water_intake_liters")
                ),
                "stress_level": FeatureBuilder._float(
                    FeatureBuilder._get(data, "stress_level")
                ),
                "screen_time_hours": FeatureBuilder._float(
                    FeatureBuilder._get(data, "screen_time_hours")
                ),
                "smoker": FeatureBuilder._bool_to_float(
                    FeatureBuilder._get(data, "smoker")
                ),
                "alcohol_use": FeatureBuilder._bool_to_float(
                    FeatureBuilder._get(data, "alcohol_use")
                ),
                "diet_quality": FeatureBuilder._float(
                    FeatureBuilder._get(data, "diet_quality")
                ),
                "fruits_per_day": FeatureBuilder._float(
                    FeatureBuilder._get(data, "fruits_per_day")
                ),
                "vegetables_per_day": FeatureBuilder._float(
                    FeatureBuilder._get(data, "vegetables_per_day")
                ),
            }

            return features

        except Exception as exc:
            raise FeatureEngineeringError(
                f"Feature building failed: {exc}"
            ) from exc

    # ==================================================
    # DATAFRAME CONVERSION
    # ==================================================

    @staticmethod
    def to_dataframe(
        features: Dict[str, float],
    ) -> pd.DataFrame:

        ordered_features = {
            col: float(features.get(col, 0.0))
            for col in FEATURE_COLUMNS
        }

        return pd.DataFrame(
            [ordered_features],
            columns=FEATURE_COLUMNS,
        )

    # ==================================================
    # FEATURE METADATA
    # ==================================================

    @staticmethod
    def get_feature_names() -> list[str]:
        return FEATURE_COLUMNS.copy()

    @staticmethod
    def empty_feature_vector() -> Dict[str, float]:

        return {
            col: 0.0
            for col in FEATURE_COLUMNS
        }

    # ==================================================
    # INTERNAL HELPERS
    # ==================================================

    @staticmethod
    def _get(
        data: Any,
        field: str,
    ) -> Any:
        """
        Supports:
        - Pydantic models
        - ORM objects
        - dict payloads
        """

        if isinstance(data, dict):
            return data.get(field)

        return getattr(data, field, None)

    @staticmethod
    def _float(
        value: Any,
    ) -> float:

        if value is None:
            return 0.0

        try:
            return float(value)
        except Exception:
            return 0.0

    @staticmethod
    def _bool_to_float(
        value: Any,
    ) -> float:

        if value is None:
            return 0.0

        try:
            return float(int(bool(value)))
        except Exception:
            return 0.0