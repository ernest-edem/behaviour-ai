from typing import Dict, Any


class PredictionComparator:
    """
    Compares Rule Engine vs ML output for drift detection.
    """

    @staticmethod
    def compare(
        rule_result: Dict[str, Any],
        ml_result: Dict[str, Any],
    ) -> Dict[str, Any]:

        rule_label = rule_result.get("predicted_disease")
        ml_label = ml_result.get("predicted_disease")

        rule_risk = rule_result.get("risk_score", 0)
        ml_risk = ml_result.get("risk_score", 0)

        return {
            "label_match": rule_label == ml_label,
            "rule_label": rule_label,
            "ml_label": ml_label,
            "risk_diff": abs(rule_risk - ml_risk),
            "rule_risk": rule_risk,
            "ml_risk": ml_risk,
        }