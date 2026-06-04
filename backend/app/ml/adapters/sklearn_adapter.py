from pathlib import Path
from typing import Any, Dict, Optional

import joblib

from app.ml.models.base_model import BaseModelInterface
from app.ml.common.exceptions import (
    ModelLoadError,
    PredictionError,
)


class SklearnAdapter(BaseModelInterface):
    """
    Generic Scikit-Learn adapter.

    Supports:
    - LogisticRegression
    - RandomForestClassifier
    - GradientBoostingClassifier
    - ExtraTreesClassifier
    - XGBoost sklearn wrapper
    - Any sklearn-compatible estimator
    """

    def __init__(
        self,
        model_name: str = "sklearn_model",
        version: str = "1.0.0",
    ) -> None:

        self._model: Optional[Any] = None

        self.model_name = model_name
        self.version = version

    # ==================================================
    # MODEL LOADING
    # ==================================================

    def load_model(
        self,
        path: str,
    ) -> None:

        try:

            model_path = Path(path)

            if not model_path.exists():
                raise ModelLoadError(
                    f"Model file not found: {path}"
                )

            self._model = joblib.load(model_path)

        except Exception as exc:
            raise ModelLoadError(
                f"Failed to load model: {exc}"
            ) from exc

    # ==================================================
    # INFERENCE
    # ==================================================

    def predict(
        self,
        features: Any,
    ) -> Any:

        if self._model is None:
            raise PredictionError(
                "Model not loaded."
            )

        try:

            prediction = self._model.predict(
                features
            )

            return prediction[0]

        except Exception as exc:
            raise PredictionError(
                f"Prediction failed: {exc}"
            ) from exc

    def predict_proba(
        self,
        features: Any,
    ) -> Dict[str, float]:

        if self._model is None:
            raise PredictionError(
                "Model not loaded."
            )

        if not hasattr(
            self._model,
            "predict_proba",
        ):
            return {}

        try:

            probabilities = (
                self._model.predict_proba(
                    features
                )[0]
            )

            classes = getattr(
                self._model,
                "classes_",
                [],
            )

            return {
                str(label): float(prob)
                for label, prob in zip(
                    classes,
                    probabilities,
                )
            }

        except Exception as exc:
            raise PredictionError(
                f"Probability prediction failed: {exc}"
            ) from exc

    # ==================================================
    # MODEL ACCESS
    # ==================================================

    @property
    def model(
        self,
    ) -> Optional[Any]:
        """
        SHAP-compatible access.

        Allows:
            adapter.model
        """

        return self._model

    def get_estimator(
        self,
    ) -> Any:
        """
        Explicit estimator access.

        Used by:
        - SHAP
        - Explainability
        - Validation
        """

        return self._model

    def is_loaded(
        self,
    ) -> bool:

        return self._model is not None

    # ==================================================
    # METADATA
    # ==================================================

    def get_metadata(
        self,
    ) -> Dict[str, Any]:

        algorithm = None

        if self._model is not None:
            algorithm = (
                self._model.__class__.__name__
            )

        return {
            "name": self.model_name,
            "version": self.version,
            "framework": "scikit-learn",
            "algorithm": algorithm,
            "loaded": self.is_loaded(),
        }