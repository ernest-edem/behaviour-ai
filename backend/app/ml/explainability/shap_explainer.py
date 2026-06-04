from typing import Any, Dict

import numpy as np
import shap


class SHAPExplainer:
    """
    Production-safe SHAP wrapper.

    Supports:
    - RandomForest
    - XGBoost
    - LightGBM
    - sklearn-compatible tree models
    - adapter-wrapped models
    - graceful fallback
    """

    def __init__(self, model: Any):
        self.model = self._unwrap_model(model)
        self.explainer = None

        try:
            self.explainer = shap.TreeExplainer(
                self.model
            )
        except Exception:
            self.explainer = None

    # ==================================================
    # MODEL UNWRAPPING
    # ==================================================

    def _unwrap_model(
        self,
        model: Any,
    ) -> Any:
        """
        Supports adapter patterns.

        Example:
            SklearnAdapter.model
            XGBoostAdapter.model
        """

        try:
            if hasattr(model, "model"):
                return model.model
        except Exception:
            pass

        return model

    # ==================================================
    # MAIN EXPLAIN
    # ==================================================

    def explain(
        self,
        feature_df,
    ) -> Dict[str, Any]:

        if (
            self.explainer is None
            or feature_df is None
            or feature_df.empty
        ):
            return self._empty_result()

        try:
            shap_values = self.explainer.shap_values(
                feature_df
            )
        except Exception:
            return self._empty_result()

        try:
            shap_values = self._normalize_shap_values(
                shap_values
            )

            values = (
                shap_values[0]
                if len(shap_values) > 0
                else np.array([])
            )

            feature_names = list(
                feature_df.columns
            )

            feature_map = {
                feature_names[i]: float(values[i])
                for i in range(
                    min(
                        len(feature_names),
                        len(values),
                    )
                )
            }

            return {
                "feature_contributions": feature_map,
                "shap_values": (
                    values.tolist()
                    if hasattr(values, "tolist")
                    else []
                ),
                "base_value": self._get_base_value(),
            }

        except Exception:
            return self._empty_result()

    # ==================================================
    # NORMALIZATION
    # ==================================================

    def _normalize_shap_values(
        self,
        shap_values: Any,
    ) -> np.ndarray:

        if isinstance(shap_values, list):
            shap_values = shap_values[0]

        shap_values = np.array(shap_values)

        if shap_values.ndim == 3:
            shap_values = shap_values[0]

        return shap_values

    # ==================================================
    # BASE VALUE
    # ==================================================

    def _get_base_value(
        self,
    ) -> float:

        try:
            base_value = (
                self.explainer.expected_value
            )

            if isinstance(
                base_value,
                (list, np.ndarray),
            ):
                base_value = base_value[0]

            return float(base_value)

        except Exception:
            return 0.0

    # ==================================================
    # FALLBACK
    # ==================================================

    def _empty_result(
        self,
    ) -> Dict[str, Any]:

        return {
            "feature_contributions": {},
            "shap_values": [],
            "base_value": 0.0,
        }