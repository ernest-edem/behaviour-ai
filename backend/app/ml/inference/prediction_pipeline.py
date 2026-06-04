from typing import Any, Dict, Optional

import numpy as np
import pandas as pd

from app.ml.preprocessing.data_cleaner import DataCleaner
from app.ml.features.feature_builder import (
    FEATURE_COLUMNS,
    FeatureBuilder,
)
from app.ml.registry.model_registry import model_registry
from app.ml.inference.prediction_result import PredictionResultDTO
from app.ml.common.exceptions import ModelNotFoundError

from app.ml.explainability.shap_explainer import SHAPExplainer
from app.ml.observability.feature_drift_monitor import (
    FeatureDriftMonitor,
)


class PredictionPipeline:
    """
    Production-grade ML pipeline.

    Guarantees:
    - Never crashes API
    - Stable feature schema
    - SHAP explainability
    - Drift monitoring
    - Shadow-safe degradation
    """

    def __init__(self) -> None:
        self.cleaner = DataCleaner()
        self.registry = model_registry

    # ==================================================
    # MAIN ENTRY
    # ==================================================

    def run(
        self,
        data: Any,
    ) -> PredictionResultDTO:

        # ==================================================
        # CLEAN INPUT
        # ==================================================

        try:
            cleaned_data = self.cleaner.clean(data)
        except Exception:
            cleaned_data = data

        # ==================================================
        # FEATURE EXTRACTION
        # ==================================================

        try:
            raw_features: Dict[str, float] = (
                FeatureBuilder.build(cleaned_data)
            )
        except Exception:
            raw_features = {}

        feature_dict = self._enforce_feature_schema(
            raw_features
        )

        # never allow empty vector
        if not any(feature_dict.values()):
            feature_dict = {
                col: 0.0
                for col in FEATURE_COLUMNS
            }

        # ==================================================
        # DRIFT MONITORING
        # ==================================================

        try:
            FeatureDriftMonitor.record(
                feature_dict
            )
        except Exception:
            pass

        # ==================================================
        # DATAFRAME
        # ==================================================

        feature_df = self._to_dataframe(
            feature_dict
        )

        # ==================================================
        # MODEL LOAD
        # ==================================================

        try:
            model = self.registry.get_active_model()

        except ModelNotFoundError:

            return PredictionResultDTO(
                feature_vector=feature_dict,
                prediction_source="ml_pipeline_no_model",
            )

        # ==================================================
        # INFERENCE
        # ==================================================

        try:

            prediction_raw = model.predict(
                feature_df
            )

            probabilities_raw = (
                self._safe_predict_proba(
                    model,
                    feature_df,
                )
            )

        except Exception:

            return PredictionResultDTO(
                feature_vector=feature_dict,
                prediction_source="ml_pipeline_inference_failed",
            )

        # ==================================================
        # NORMALIZATION
        # ==================================================

        predicted_disease = (
            self._normalize_prediction(
                prediction_raw
            )
        )

        probabilities = (
            self._normalize_probabilities(
                model,
                probabilities_raw,
            )
        )

        ai_confidence = (
            self._compute_confidence(
                probabilities
            )
        )

        # ==================================================
        # SHAP EXPLAINABILITY
        # ==================================================

        shap_result = {
            "feature_contributions": {},
            "shap_values": [],
            "base_value": 0.0,
        }

        try:

            explainer = SHAPExplainer(
                model
            )

            shap_result = explainer.explain(
                feature_df
            )

        except Exception:
            pass

        # ==================================================
        # MODEL METADATA
        # ==================================================

        try:
            metadata = model.get_metadata()
        except Exception:
            metadata = {}

        # ==================================================
        # DTO
        # ==================================================

        return PredictionResultDTO(
            predicted_disease=predicted_disease,
            ai_confidence=ai_confidence,
            disease_probabilities=probabilities,
            feature_vector=feature_dict,
            feature_contributions=shap_result.get(
                "feature_contributions"
            ),
            shap_values=shap_result.get(
                "shap_values"
            ),
            model_name=metadata.get(
                "name"
            ),
            model_type=metadata.get(
                "framework"
            ),
            model_version=metadata.get(
                "version",
                "1.0.0",
            ),
            prediction_source="ml_pipeline",
        )

    # ==================================================
    # FEATURE SCHEMA
    # ==================================================

    def _enforce_feature_schema(
        self,
        features: Dict[str, float],
    ) -> Dict[str, float]:

        safe_features: Dict[str, float] = {}

        for col in FEATURE_COLUMNS:

            value = features.get(col)

            if value is None:
                safe_features[col] = 0.0
                continue

            try:
                safe_features[col] = float(
                    value
                )
            except Exception:
                safe_features[col] = 0.0

        return safe_features

    # ==================================================
    # DATAFRAME
    # ==================================================

    def _to_dataframe(
        self,
        feature_dict: Dict[str, float],
    ) -> pd.DataFrame:

        try:

            row = [[
                feature_dict[col]
                for col in FEATURE_COLUMNS
            ]]

            return pd.DataFrame(
                row,
                columns=FEATURE_COLUMNS,
            )

        except Exception:

            return pd.DataFrame(
                columns=FEATURE_COLUMNS
            )

    # ==================================================
    # MODEL SAFE CALLS
    # ==================================================

    def _safe_predict_proba(
        self,
        model,
        X,
    ) -> Optional[Any]:

        if not hasattr(
            model,
            "predict_proba",
        ):
            return None

        try:
            return model.predict_proba(X)
        except Exception:
            return None

    # ==================================================
    # NORMALIZATION
    # ==================================================

    def _normalize_prediction(
        self,
        prediction_raw: Any,
    ) -> str:

        if prediction_raw is None:
            return "unknown"

        if isinstance(
            prediction_raw,
            (
                list,
                tuple,
                np.ndarray,
            ),
        ):
            return (
                str(prediction_raw[0])
                if len(prediction_raw) > 0
                else "unknown"
            )

        return str(prediction_raw)

    def _normalize_probabilities(
        self,
        model,
        probs: Any,
    ) -> Dict[str, float]:

        if probs is None:
            return {}

        if isinstance(
            probs,
            dict,
        ):
            return {
                k: float(v)
                for k, v in probs.items()
            }

        try:

            if isinstance(
                probs,
                np.ndarray,
            ):

                classes = getattr(
                    model,
                    "classes_",
                    None,
                )

                if classes is not None:

                    return {
                        str(classes[i]): float(v)
                        for i, v in enumerate(
                            probs[0]
                        )
                    }

                return {
                    f"class_{i}": float(v)
                    for i, v in enumerate(
                        probs[0]
                    )
                }

        except Exception:
            pass

        return {}

    def _compute_confidence(
        self,
        probabilities: Dict[str, float],
    ) -> float:

        if not probabilities:
            return 0.0

        try:
            return float(
                max(
                    probabilities.values()
                )
            )
        except Exception:
            return 0.0