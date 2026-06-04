from typing import Dict, Any

from app.ml.feature_engineering.feature_builder import FeatureBuilder
from app.ml.explainability.shap_engine import SHAPEngine


class ExplanationService:
    """
    Converts model predictions → clinical explanations
    """

    def __init__(self, model, feature_names):
        self.shap_engine = SHAPEngine(model, feature_names)

    def explain_prediction(self, features: Dict[str, float]) -> Dict[str, Any]:

        # Convert to model input
        df = FeatureBuilder.to_dataframe(features)

        # SHAP expects numpy array
        shap_values = self.shap_engine.explain(df.values)

        # Sort risk drivers
        sorted_features = sorted(
            shap_values.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )

        return {
            "risk_drivers": [
                {
                    "feature": k,
                    "impact": v
                }
                for k, v in sorted_features[:5]
            ],
            "shap_values": shap_values
        }