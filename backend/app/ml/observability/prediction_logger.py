from datetime import datetime
from typing import Any, Dict


class PredictionLogger:
    """
    Captures full ML audit trail per prediction.
    """

    @staticmethod
    def log(
        user_id: int,
        input_data: Dict,
        feature_vector: Dict,
        result: Dict,
    ) -> Dict[str, Any]:

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "input": input_data,
            "features": feature_vector,
            "output": result,
            "model_version": result.get("model_version"),
            "risk_score": result.get("risk_score"),
            "prediction_source": result.get("prediction_source"),
        }