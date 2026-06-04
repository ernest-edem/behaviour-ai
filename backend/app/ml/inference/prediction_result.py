from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class PredictionResultDTO:
    """
    Canonical prediction object used throughout the
    BehaviorLens AI prediction pipeline.

    Used by:
    - Rule Engine
    - PredictionPipeline
    - PredictionOrchestrator
    - Model Adapters
    - FastAPI Routers
    - Future SHAP Explainability Engine
    """

    # ==================================================
    # IDENTIFIERS
    # ==================================================

    prediction_id: Optional[int] = None

    # ==================================================
    # PRIMARY PREDICTION
    # ==================================================

    predicted_disease: str = ""

    health_score: float = 0.0

    risk_score: float = 0.0

    ai_confidence: float = 0.0

    risk_level: str = "Low"

    urgency: str = "Low"

    # ==================================================
    # BEHAVIORAL ANALYTICS
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
    # FUTURE EXPLAINABILITY
    # ==================================================

    feature_contributions: Dict[str, float] = field(
        default_factory=dict
    )

    shap_values: Dict[str, float] = field(
        default_factory=dict
    )

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
        """
        Canonical API payload.
        """

        return asdict(self)

    def to_legacy_dict(self) -> Dict[str, Any]:
        """
        Legacy payload used by existing frontend
        during migration.
        """

        return {
            **self.to_dict(),

            "predicted_disease":
                self.predicted_disease,

            "ai_confidence":
                round(
                    self.ai_confidence,
                    2
                ),

            "explanation":
                self.explanations,

            "recommendation":
                " ".join(self.recommendations)
                if self.recommendations
                else "",
        }

    @classmethod
    def from_rule_engine(
        cls,
        result: Dict[str, Any],
        feature_vector: Optional[
            Dict[str, float]
        ] = None,
    ) -> "PredictionResultDTO":
        """
        Convert legacy rule engine output
        into the canonical DTO.
        """

        return cls(
            prediction_id=result.get(
                "prediction_id"
            ),

            predicted_disease=result.get(
                "predicted_disease",
                result.get(
                    "predicted_disease",
                    ""
                ),
            ),

            health_score=result.get(
                "health_score",
                0.0,
            ),

            risk_score=result.get(
                "risk_score",
                0.0,
            ),

            ai_confidence=result.get(
                "ai_confidence",
                result.get(
                    "ai_confidence",
                    0.0,
                ) / 100,
            ),

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
                    ""
                )
            ]
            if result.get(
                "recommendation"
            )
            else [],

            explanations=result.get(
                "explanations",
                result.get(
                    "explanation",
                    [],
                ),
            ),

            feature_vector=feature_vector
            or {},

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