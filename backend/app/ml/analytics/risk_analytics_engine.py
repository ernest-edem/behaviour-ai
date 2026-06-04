from typing import List, Dict
import numpy as np
from datetime import datetime, timedelta


class RiskAnalyticsEngine:
    """
    Converts raw historical risk scores into
    clinical longitudinal intelligence.
    """

    # =====================================================
    # MAIN ENTRY
    # =====================================================

    def analyze(self, records: List) -> Dict:
        """
        records: List of PredictionHistory OR RiskTrend rows
        """

        if not records:
            return self._empty()

        scores = [r.risk_score for r in records]

        return {
            "trend": self._trend(scores),
            "moving_averages": self._moving_averages(scores),
            "volatility": self._volatility(scores),
            "trajectory": self._trajectory(scores),
        }

    # =====================================================
    # TREND CLASSIFICATION
    # =====================================================

    def _trend(self, scores: List[float]) -> str:

        if len(scores) < 2:
            return "stable"

        slope = np.mean(np.diff(scores))

        if slope > 0.05:
            return "worsening"
        elif slope < -0.05:
            return "improving"
        else:
            return "stable"

    # =====================================================
    # MOVING AVERAGES
    # =====================================================

    def _moving_averages(self, scores: List[float]) -> Dict:

        def avg(window):
            return float(np.mean(window)) if window else 0.0

        return {
            "7_day": avg(scores[-7:]),
            "30_day": avg(scores[-30:]),
        }

    # =====================================================
    # VOLATILITY (RISK INSTABILITY)
    # =====================================================

    def _volatility(self, scores: List[float]) -> float:
        return float(np.std(scores)) if len(scores) > 1 else 0.0

    # =====================================================
    # TRAJECTORY (CLINICAL SIGNAL)
    # =====================================================

    def _trajectory(self, scores: List[float]) -> str:

        if len(scores) < 5:
            return "insufficient_data"

        recent = np.mean(scores[-3:])
        past = np.mean(scores[:-3])

        diff = recent - past

        if diff > 0.1:
            return "rapid_deterioration"
        elif diff < -0.1:
            return "rapid_improvement"
        else:
            return "stable_progression"

    # =====================================================
    # EMPTY STATE
    # =====================================================

    def _empty(self):
        return {
            "trend": "stable",
            "moving_averages": {
                "7_day": 0.0,
                "30_day": 0.0
            },
            "volatility": 0.0,
            "trajectory": "insufficient_data"
        }