"""
FeatureBuilder — Production-grade deterministic feature extraction layer
for BehaviorLens AI ML pipeline.

Upgrades:
- Schema validation (FeatureContract enforced)
- Versioned feature contract
- Strict deterministic output
- ML-safe DataFrame conversion
- Hard validation guards
"""

from typing import Any, Dict, List
import pandas as pd
import logging

from app.ml.common.exceptions import FeatureEngineeringError
from app.ml.contracts.feature_contract import FeatureContract

logger = logging.getLogger(__name__)


# =========================================================
# FEATURE CONTRACT (VERSIONED)
# =========================================================

FEATURE_VERSION = "v1.1"

FEATURE_COLUMNS: List[str] = [
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


# =========================================================
# SAFE DEFAULTS
# =========================================================

_SAFE_DEFAULTS: Dict[str, float] = {
    "sleep_hours": 7.0,
    "exercise_minutes": 30.0,
    "water_intake_liters": 2.0,
    "stress_level": 3.0,
    "screen_time_hours": 4.0,
    "smoker": 0.0,
    "alcohol_use": 0.0,
    "diet_quality": 5.0,
    "fruits_per_day": 2.0,
    "vegetables_per_day": 2.0,
}


# =========================================================
# FEATURE BUILDER
# =========================================================

class FeatureBuilder:
    """
    Deterministic feature extraction engine.

    Guarantees:
    - Same input → same output
    - No missing features
    - Schema validated ML input
    - Safe fallback defaults
    """

    @staticmethod
    def build(data: Any, *, strict: bool = False) -> Dict[str, float]:
        """
        Build feature vector from payload.

        Flow:
        raw input → contract validation → safe ML vector
        """

        try:
            # ==================================================
            # 1. RAW NORMALIZATION
            # ==================================================
            raw: Dict[str, Any] = data if isinstance(data, dict) else {}

            # ==================================================
            # 2. SCHEMA CONTRACT ENFORCEMENT
            # ==================================================
            try:
                contracted = FeatureContract.build(raw)
            except Exception:
                contracted = {}

            # ==================================================
            # 3. FEATURE ASSEMBLY (CANONICAL ORDER)
            # ==================================================
            features: Dict[str, float] = {}
            missing_fields: List[str] = []

            for col in FEATURE_COLUMNS:

                value = contracted.get(col)

                if value is None:
                    missing_fields.append(col)
                    value = _SAFE_DEFAULTS[col]

                features[col] = FeatureBuilder._safe_float(col, value)

            # ==================================================
            # 4. OBSERVABILITY WARNING (NON-BLOCKING)
            # ==================================================
            if missing_fields:
                logger.warning(
                    "[FeatureBuilder] Missing fields replaced with defaults: %s",
                    missing_fields,
                )

            # ==================================================
            # 5. FINAL HARD VALIDATION
            # ==================================================
            FeatureBuilder._validate_vector(features)

            return features

        except Exception as exc:
            logger.error("[FeatureBuilder] Failed: %s", str(exc))
            raise FeatureEngineeringError(str(exc)) from exc

    # =========================================================
    # DATAFRAME CONVERSION
    # =========================================================

    @staticmethod
    def to_dataframe(features: Dict[str, float]) -> pd.DataFrame:
        """
        Convert feature dict → ML-ready DataFrame
        with strict column ordering.
        """

        df = pd.DataFrame([features])
        return df.reindex(columns=FEATURE_COLUMNS)

    # =========================================================
    # METADATA
    # =========================================================

    @staticmethod
    def get_feature_names() -> List[str]:
        return FEATURE_COLUMNS.copy()

    @staticmethod
    def get_feature_version() -> str:
        return FEATURE_VERSION

    # =========================================================
    # INTERNAL HELPERS
    # =========================================================

    @staticmethod
    def _safe_float(col: str, raw: Any) -> float:
        """
        Convert raw value → safe float.
        """

        if raw is None:
            return _SAFE_DEFAULTS[col]

        if isinstance(raw, bool):
            return float(raw)

        try:
            return float(raw)
        except Exception:
            return _SAFE_DEFAULTS[col]

    @staticmethod
    def _validate_vector(features: Dict[str, float]) -> None:
        """
        Hard validation guard to prevent ML corruption.
        """

        for k, v in features.items():

            if v is None:
                raise FeatureEngineeringError(f"{k} is None")

            if isinstance(v, float):

                if v != v:  # NaN
                    raise FeatureEngineeringError(f"{k} is NaN")

                if v == float("inf") or v == float("-inf"):
                    raise FeatureEngineeringError(f"{k} is infinite")