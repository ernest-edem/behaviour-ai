from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class PredictionResultDTO:
    """
    Canonical prediction object.

    Single source of truth across:

    - Rule Engine
    - ML Pipeline
    - Orchestrator
    - Explainability
    - API Layer
    """

    # ==================================================
    # IDENTIFIERS
    # ==================================================

    prediction_id: Optional[int] = None

    # ==================================================
    # PRIMARY PREDICTION
    # ==================================================

    predicted_disease: str = ""

    predicted_condition: str = ""

    health_score: float = 0.0

    risk_score: float = 0.0

    ai_confidence: float = 0.0

    confidence_score: float = 0.0

    risk_level: str = "Low"

    urgency: str = "Low"

    # ==================================================
    # BEHAVIORAL
    # ==================================================

    behavioral_phenotype: Optional[str] = None

    # ==================================================
    # MODEL OUTPUT
    # ==================================================

    disease_probabilities: Dict[str, float] = field(
        default_factory=dict
    )

    recommendations: List[str] = field(
        default_factory=list
    )

    explanations: List[str] = field(
        default_factory=list
    )

    # ==================================================
    # FEATURES
    # ==================================================

    feature_vector: Dict[str, float] = field(
        default_factory=dict
    )

    # ==================================================
    # EXPLAINABILITY
    # ==================================================

    feature_contributions: Dict[str, float] = field(
        default_factory=dict
    )

    shap_values: List[float] = field(
        default_factory=list
    )

    shap_base_value: float = 0.0

    # ==================================================
    # MODEL METADATA
    # ==================================================

    prediction_source: str = "rule_engine"

    model_name: Optional[str] = None

    model_type: Optional[str] = None

    model_version: str = "v1.0"

    # ==================================================
    # AUDIT
    # ==================================================

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    # ==================================================
    # SERIALIZATION
    # ==================================================

    def to_dict(self) -> Dict[str, Any]:

        return asdict(self)

    def to_legacy_dict(self) -> Dict[str, Any]:

        return {
            **self.to_dict(),

            "predicted_disease":
                self.predicted_disease,

            "predicted_condition":
                self.predicted_condition,

            "ai_confidence":
                round(self.ai_confidence, 2),

            "confidence_score":
                round(self.confidence_score, 2),

            "explanation":
                self.explanations,

            "recommendation":
                " ".join(self.recommendations)
                if self.recommendations
                else "",
        }

    # ==================================================
    # FACTORY
    # ==================================================

    @classmethod
    def from_rule_engine(
        cls,
        result: Dict[str, Any],
        feature_vector: Optional[
            Dict[str, float]
        ] = None,
    ) -> "PredictionResultDTO":

        confidence = float(
            result.get(
                "ai_confidence",
                0.0,
            )
        )

        explanations = result.get(
            "explanations"
        )

        if explanations is None:

            explanation = result.get(
                "explanation"
            )

            if isinstance(explanation, str):
                explanations = [explanation]
            elif isinstance(explanation, list):
                explanations = explanation
            else:
                explanations = []

        predicted_disease = result.get(
            "predicted_disease",
            "",
        )

        return cls(

            prediction_id=result.get(
                "prediction_id"
            ),

            predicted_disease=
                predicted_disease,

            predicted_condition=
                predicted_disease,

            health_score=float(
                result.get(
                    "health_score",
                    0.0,
                )
            ),

            risk_score=float(
                result.get(
                    "risk_score",
                    0.0,
                )
            ),

            ai_confidence=confidence,

            confidence_score=confidence,

            risk_level=result.get(
                "risk_level",
                "Low",
            ),

            urgency=result.get(
                "urgency",
                "Low",
            ),

            behavioral_phenotype=result.get(
                "behavioral_phenotype"
            ),

            disease_probabilities=result.get(
                "disease_probabilities",
                {},
            ),

            recommendations=[
                result.get(
                    "recommendation",
                    "",
                )
            ]
            if result.get(
                "recommendation"
            )
            else [],

            explanations=explanations,

            feature_vector=feature_vector or {},

            feature_contributions=result.get(
                "feature_contributions",
                {},
            ),

            shap_values=result.get(
                "shap_values",
                [],
            ),

            shap_base_value=float(
                result.get(
                    "shap_base_value",
                    0.0,
                )
            ),

            prediction_source=result.get(
                "prediction_source",
                "rule_engine",
            ),

            model_name=result.get(
                "model_name"
            ),

            model_type=result.get(
                "model_type"
            ),

            model_version=result.get(
                "model_version",
                "rule-engine-v1",
            ),
        )