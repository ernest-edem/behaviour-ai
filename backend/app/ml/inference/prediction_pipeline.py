# backend/app/ml/inference/prediction_pipeline.py

from typing import Any, Dict

from app.ml.preprocessing.data_cleaner import DataCleaner
from app.ml.feature_engineering.feature_builder import FeatureBuilder
from app.ml.registry.model_registry import model_registry
from app.ml.inference.prediction_result import PredictionResultDTO


class PredictionPipeline:
    """
    Core ML pipeline.

    Responsibilities:
    - Clean input
    - Build features
    - Run model inference
    - Return structured DTO
    """

    def __init__(self) -> None:
        self.cleaner = DataCleaner()
        self.feature_builder = FeatureBuilder()
        self.registry = model_registry

    def run(self, data: Any) -> PredictionResultDTO:
        """
        Execute full ML pipeline.
        """

        # 1. Clean input
        cleaned_data = self.cleaner.clean(data)

        # 2. Build feature dict (SHAP-ready)
        feature_dict: Dict[str, float] = self.feature_builder.build(cleaned_data)

        # 3. Convert to DataFrame for sklearn
        feature_df = self.feature_builder.to_dataframe(feature_dict)

        # 4. Get active model
        model = self.registry.get_active_model()

        # 5. ML inference
        prediction = model.predict(feature_df)
        probabilities = model.predict_proba(feature_df)

        # 6. Basic scoring logic (temporary fallback until SHAP layer)
        ai_confidence = max(probabilities.values()) if probabilities else 0.0

        # 7. Build DTO 
        return PredictionResultDTO(
            predicted_disease=str(prediction),
            ai_confidence=ai_confidence,
            disease_probabilities=probabilities,
            feature_vector=feature_dict,
            model_name=model.get_metadata().get("name"),
            model_type=model.get_metadata().get("framework"),
            model_version=model.get_metadata().get("version", "1.0.0"),
            prediction_source="ml_pipeline",
        )