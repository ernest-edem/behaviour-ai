from typing import Dict, Any

from app.domains.phenotypes.phenotype_types import PhenotypeType
from app.domains.phenotypes.phenotype_scoring import PhenotypeScoringEngine
from app.domains.phenotypes.phenotype_hybrid_scoring import PhenotypeHybridScoringEngine
from app.ml.inference.prediction_result import PredictionResultDTO


class PhenotypeService:
    """
    Phase 4 Step C Upgrade:
    Hybrid Intelligence Layer
    """

    def __init__(self):
        self.rule_scorer = PhenotypeScoringEngine()
        self.hybrid_scorer = PhenotypeHybridScoringEngine()

    def generate(self, prediction: PredictionResultDTO) -> Dict[str, Any]:

        features = prediction.feature_vector

        # 1. Rule-based scores
        rule_scores = self.rule_scorer.score(features)

        # 2. Hybrid intelligence scores (NEW)
        hybrid_scores = self.hybrid_scorer.score(features)

        phenotype, confidence = self._select_top(hybrid_scores)

        return {
            "phenotype": phenotype.value,
            "confidence": confidence,

            "risk_score": prediction.risk_score,

            # Phase 4 upgrade signals
            "rule_scores": rule_scores,
            "hybrid_scores": hybrid_scores["feature_contributions"],

            "overall_risk": hybrid_scores["overall_risk"],

            "signals": self._extract_signals(features),
        }

    def _select_top(self, scores: Dict[str, float]):

        # Use rule + hybrid fusion (weighted decision)
        score_map = {
            "burnout": scores.get("stress_signal", 0),
            "overwhelmed": scores.get("stress_signal", 0) * 0.9,
            "non_adherent": scores.get("diet_risk_signal", 0),
            "cardiometabolic": scores.get("overall_risk", 0),
            "prevention": 1 - scores.get("overall_risk", 0),
        }

        best_key = max(score_map, key=score_map.get)
        best_score = score_map[best_key]

        mapping = {
            "burnout": PhenotypeType.BURNOUT_PRONE,
            "overwhelmed": PhenotypeType.EMOTIONALLY_OVERWHELMED,
            "non_adherent": PhenotypeType.DISTRESSED_NON_ADHERENT,
            "cardiometabolic": PhenotypeType.HIGH_CARDIOMETABOLIC_RISK,
            "prevention": PhenotypeType.PREVENTION_OPPORTUNITY,
        }

        return mapping[best_key], best_score

    def _extract_signals(self, features: Dict[str, float]) -> Dict[str, float]:

        return {
            "stress": features.get("stress_level", 0),
            "sleep": features.get("sleep_hours", 0),
            "screen_time": features.get("screen_time_hours", 0),
            "exercise": features.get("exercise_minutes", 0),
            "diet": features.get("diet_quality", 0),
        }