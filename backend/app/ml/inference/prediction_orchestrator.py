from typing import Any, Dict

from app.ml.inference.prediction_pipeline import PredictionPipeline
from app.ml.inference.prediction_result import PredictionResultDTO

from app.ml.rule_engine import generate_prediction as rule_engine_prediction
from app.domains.phenotypes.phenotype_service import PhenotypeService
from app.ml.features.feature_builder import FeatureBuilder
from app.ml.contracts.feature_contract import FeatureContract


class PredictionOrchestrator:
    """
    Production orchestration layer.

    Flow:
        Rule Engine → FeatureBuilder → Contract Validation
              ↓
        DTO (Canonical State)
              ↓
        ML Pipeline (Shadow Mode)
              ↓
        Phenotype Engine (Feature-driven)
              ↓
        Normalized API Response
    """

    def __init__(self) -> None:
        self.pipeline = PredictionPipeline()
        self.phenotype_service = PhenotypeService()

    def predict(self, data: Any) -> Dict[str, Any]:

        # ==================================================
        # 1. RULE ENGINE (PRIMARY SOURCE OF TRUTH)
        # ==================================================
        legacy_result: Dict[str, Any] = rule_engine_prediction(data)

        # ==================================================
        # 2. FEATURE VECTOR (STRICT GUARANTEE LAYER)
        # ==================================================
        raw_features = FeatureBuilder.build(data)
        feature_vector: Dict[str, float] = FeatureContract.build(raw_features)

        # HARD SAFETY: NEVER ALLOW EMPTY VECTOR INTO SYSTEM
        if not isinstance(feature_vector, dict) or len(feature_vector) == 0:
            feature_vector = {
                "sleep_hours": 7.0,
                "exercise_minutes": 30.0,
                "water_intake_liters": 2.0,
                "stress_level": 3.0,
                "screen_time_hours": 4.0,
                "smoker": 0.0,
                "alcohol_use": 0.0,
                "diet_quality": 5.0,
                "fruits_per_day": 2.0,
                "vegetables_per_day": 2.0,
            }

        # ==================================================
        # 3. DTO CREATION (CANONICAL STATE)
        # ==================================================
        dto = PredictionResultDTO.from_rule_engine(
            legacy_result,
            feature_vector=feature_vector,
        )

        response = dto.to_legacy_dict()

        # SINGLE SOURCE OF TRUTH FOR FEATURE VECTOR
        response["feature_vector"] = dto.feature_vector

        # ==================================================
        # 4. SHADOW ML PIPELINE (NEVER BREAK PROD)
        # ==================================================
        try:
            ml_result = self.pipeline.run(data)

            response.update({
                "ml_feature_vector": ml_result.feature_vector,
                "ml_model_version": ml_result.model_version,
                "ml_prediction_source": ml_result.prediction_source,
            })

        except Exception:
            response.update({
                "ml_feature_vector": dto.feature_vector,
                "ml_model_version": "shadow-fallback",
                "ml_prediction_source": "fallback",
            })

        # ==================================================
        # 5. PHENOTYPE ENGINE (FEATURE-DRIVEN)
        # ==================================================
        try:
            phenotype_result = self.phenotype_service.generate(dto)

            response["behavioral_phenotype"] = phenotype_result.get("phenotype")

            response["behavioral_profile"] = {
                "phenotype": phenotype_result.get("phenotype"),
                "confidence": phenotype_result.get("confidence", 0.0),
                "risk_score": phenotype_result.get("risk_score", 0.0),
                "signals": phenotype_result.get("signals", []),
                "scores": phenotype_result.get("scores", {}),
            }

        except Exception as exc:

            response["behavioral_phenotype"] = legacy_result.get("behavioral_phenotype")

            response["behavioral_profile"] = {
                "error": str(exc)
            }

        # ==================================================
        # 6. CANONICAL FIELD NORMALIZATION
        # ==================================================
        response["predicted_condition"] = response.get("predicted_disease")
        response["confidence_score"] = response.get("ai_confidence")
        response.setdefault("prediction_source", "rule_engine")

        return response