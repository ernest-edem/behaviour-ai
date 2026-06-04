from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseModelInterface(ABC):
    """
    Abstract contract for all ML model adapters.

    This interface decouples the prediction pipeline from
    specific ML frameworks such as:

    - Scikit-learn
    - Random Forest
    - XGBoost
    - LightGBM
    - Future Deep Learning Models

    All concrete adapters must implement these methods.
    """

    @abstractmethod
    def load_model(self, path: str) -> None:
        """
        Load a serialized model from disk.

        Args:
            path: Absolute or relative path to the model artifact.

        Raises:
            ModelLoadError
        """
        pass

    @abstractmethod
    def predict(self, features: Any) -> Any:
        """
        Generate the primary prediction.

        Args:
            features:
                Feature matrix or dataframe.

        Returns:
            Predicted class/label.
        """
        pass

    @abstractmethod
    def predict_proba(self, features: Any) -> Dict[str, float]:
        """
        Generate class probability predictions.

        Args:
            features:
                Feature matrix or dataframe.

        Returns:
            Dictionary of:

            {
                "diabetes": 0.72,
                "hypertension": 0.18,
                "obesity": 0.10
            }
        """
        pass

    @abstractmethod
    def get_estimator(self) -> Any:
        """
        Return the underlying ML estimator.

        Required for:

        - SHAP
        - Feature importance
        - Model inspection
        - Advanced explainability

        Returns:
            Raw sklearn/xgboost estimator instance.
        """
        pass

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """
        Return runtime model metadata.

        Example:
        {
            "name": "behavior_model",
            "version": "1.0.0",
            "framework": "scikit-learn",
            "algorithm": "RandomForestClassifier"
        }
        """
        pass