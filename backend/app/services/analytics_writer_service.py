from sqlalchemy.orm import Session
from datetime import datetime

from app.models.risk_trend import RiskTrend
from app.models.intervention_log import InterventionLog
from app.ml.analytics.risk_trend_service import RiskTrendService


class AnalyticsWriterService:

    def __init__(self):
        self.trend_engine = RiskTrendService()

    # =====================================================
    # RISK TREND PERSISTENCE
    # =====================================================

    def write_risk_trend(
        self,
        db: Session,
        user_id: int,
        disease_name: str,
        scores: list[float],
    ):
        trend = self.trend_engine.compute(scores)

        record = RiskTrend(
            user_id=user_id,
            disease_name=disease_name,
            risk_score=scores[-1] if scores else 0,
            trend_direction=trend["trend"],
            moving_average_7d=trend["moving_average_7d"],
            moving_average_30d=trend["moving_average_30d"],
            volatility_score=trend["volatility_score"],
            created_at=datetime.utcnow(),
        )

        db.add(record)
        return record

    # =====================================================
    # INTERVENTION TRACKING ENGINE
    # =====================================================

    def log_intervention(
        self,
        db: Session,
        user_id: int,
        intervention_type: str,
        trigger_source: str,
        description: str,
        effectiveness_score: float = 0.0,
        status: str = "active",
    ):

        log = InterventionLog(
            user_id=user_id,
            intervention_type=intervention_type,
            trigger_source=trigger_source,
            description=description,
            effectiveness_score=effectiveness_score,
            status=status,
            created_at=datetime.utcnow(),
        )

        db.add(log)
        return log

    # =====================================================
    # AUTO-INTERVENTION ENGINE (CLINICAL LOGIC)
    # =====================================================

    def auto_generate_interventions(
        self,
        db: Session,
        user_id: int,
        result: dict,
    ):

        interventions = []

        risk = result.get("risk_score", 0)
        condition = result.get("predicted_disease", "")

        # High risk trigger
        if risk >= 70:
            interventions.append(
                self.log_intervention(
                    db,
                    user_id,
                    "alert",
                    "risk_engine",
                    f"High risk detected for {condition}",
                    0.0,
                )
            )

        # Stress-based trigger
        if result.get("behavioral_phenotype", "").lower().find("overwhelmed") != -1:
            interventions.append(
                self.log_intervention(
                    db,
                    user_id,
                    "lifestyle_change",
                    "behavior_engine",
                    "Stress management intervention recommended",
                    0.0,
                )
            )

        # Low adherence / general prevention
        if risk < 30:
            interventions.append(
                self.log_intervention(
                    db,
                    user_id,
                    "prevention",
                    "analytics_engine",
                    "Maintain current healthy lifestyle",
                    0.0,
                )
            )

        return interventions