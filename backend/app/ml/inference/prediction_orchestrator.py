from typing import Any, Dict

from app.ml.inference.prediction_pipeline import PredictionPipeline
from app.ml.inference.prediction_result import PredictionResultDTO

from app.ml.rule_engine import (
    generate_prediction as rule_engine_prediction
)

from app.domains.phenotypes.phenotype_service import (
    PhenotypeService
)


class PredictionOrchestrator:
    """
    Production orchestration layer.

    Flow:

        Rule Engine (source of truth)
                ↓
        PredictionResultDTO
                ↓
        ML Pipeline (shadow mode)
                ↓
        Phenotype Engine
                ↓
        API Response

    Requirements:

    - Never break existing API
    - Rule engine remains primary
    - ML runs in shadow mode
    - Supports future SHAP integration
    """

    def __init__(self) -> None:
        self.pipeline = PredictionPipeline()
        self.phenotype_service = PhenotypeService()

    def predict(self, data: Any) -> Dict[str, Any]:

        # ==================================================
        # PRIMARY PRODUCTION PREDICTION
        # ==================================================

        legacy_result: Dict[str, Any] = (
            rule_engine_prediction(data)
        )

        dto = PredictionResultDTO.from_rule_engine(
            legacy_result
        )

        response = dto.to_legacy_dict()

        # ==================================================
        # ML PIPELINE (SHADOW MODE)
        # ==================================================

        try:

            ml_result = self.pipeline.run(data)

            response["ml_feature_vector"] = (
                ml_result.feature_vector
            )

            response["ml_model_version"] = (
                ml_result.model_version
            )

            response["ml_prediction_source"] = (
                ml_result.prediction_source
            )

        except Exception:
            pass

        # ==================================================
        # PHENOTYPE ENGINE
        # ==================================================

        try:

            phenotype_result = (
                self.phenotype_service.generate(dto)
            )

            phenotype_name = phenotype_result.get(
                "phenotype"
            )

            response["behavioral_phenotype"] = (
                phenotype_name
            )

            # legacy compatibility
            response["behavioral_profile"] = {
                "phenotype": phenotype_name,
                "confidence": phenotype_result.get(
                    "confidence"
                ),
                "risk_score": phenotype_result.get(
                    "risk_score"
                ),
                "signals": phenotype_result.get(
                    "signals",
                    [],
                ),
                "scores": phenotype_result.get(
                    "scores",
                    {},
                ),
            }

        except Exception:

            response.setdefault(
                "behavioral_phenotype",
                legacy_result.get(
                    "behavioral_phenotype"
                ),
            )

            response["behavioral_profile"] = None

        # ==================================================
        # CANONICAL FIELD NORMALIZATION
        # ==================================================

        response["predicted_condition"] = response.get(
            "predicted_disease"
        )

        response["confidence_score"] = response.get(
            "ai_confidence"
        )

        response.setdefault(
            "prediction_source",
            "rule_engine",
        )

        return response