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
    - Any sklearn-compatible estimator
    """

    def __init__(
        self,
        model_name: str = "sklearn_model",
        version: str = "1.0.0",
    ):
        self._model: Optional[Any] = None

        self.model_name = model_name
        self.version = version

    def load_model(self, path: str) -> None:
        """
        Load serialized sklearn model.
        """

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

    def predict(self, features: Any) -> Any:
        """
        Return primary prediction.
        """

        if self._model is None:
            raise PredictionError(
                "Model not loaded."
            )

        try:
            prediction = self._model.predict(features)

            return prediction[0]

        except Exception as exc:
            raise PredictionError(
                f"Prediction failed: {exc}"
            ) from exc

    def predict_proba(
        self,
        features: Any,
    ) -> Dict[str, float]:
        """
        Return class probabilities.
        """

        if self._model is None:
            raise PredictionError(
                "Model not loaded."
            )

        try:
            probabilities = self._model.predict_proba(
                features
            )[0]

            classes = self._model.classes_

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

    def get_estimator(self) -> Any:
        """
        Required for SHAP.
        """

        return self._model

    def get_metadata(self) -> Dict[str, Any]:
        """
        Runtime model metadata.
        """

        algorithm = None

        if self._model is not None:
            algorithm = self._model.__class__.__name__

        return {
            "name": self.model_name,
            "version": self.version,
            "framework": "scikit-learn",
            "algorithm": algorithm,
        }