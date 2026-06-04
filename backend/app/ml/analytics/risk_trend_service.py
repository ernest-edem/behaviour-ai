from typing import List, Dict
import numpy as np


class RiskTrendService:

    def compute(self, scores: List[float]) -> Dict:

        if len(scores) < 2:
            return {"trend": "stable", "volatility": 0.0}

        diff = np.diff(scores)

        avg_change = np.mean(diff)
        volatility = np.std(scores)

        if avg_change > 0.05:
            trend = "worsening"
        elif avg_change < -0.05:
            trend = "improving"
        else:
            trend = "stable"

        return {
            "trend": trend,
            "volatility": float(volatility),
            "avg_change": float(avg_change)
        }