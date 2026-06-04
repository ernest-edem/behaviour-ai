from typing import List, Dict


class AnalyticsEngine:
    """
    Phase 6 Core Engine:
    - Computes longitudinal health analytics
    - Produces trends
    - Generates intervention signals
    """

    def compute_trends(self, scores: List[float]) -> Dict:

        if not scores:
            return {
                "trend": "stable",
                "moving_average_7d": 0,
                "moving_average_30d": 0,
                "volatility_score": 0,
            }

        def moving_average(window: int):
            return sum(scores[-window:]) / min(window, len(scores))

        latest = scores[-1]
        first = scores[0]

        # Trend direction
        if latest > first + 5:
            trend = "worsening"
        elif latest < first - 5:
            trend = "improving"
        else:
            trend = "stable"

        # Volatility
        avg = sum(scores) / len(scores)
        variance = sum((x - avg) ** 2 for x in scores) / len(scores)
        volatility = round(variance ** 0.5, 2)

        return {
            "trend": trend,
            "moving_average_7d": moving_average(7),
            "moving_average_30d": moving_average(30),
            "volatility_score": volatility,
        }