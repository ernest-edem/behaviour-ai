from sqlalchemy.orm import Session
from typing import Dict

from app.models.prediction import Prediction
from app.models.prediction_history import PredictionHistory
from app.models.risk_trend import RiskTrend
from app.models.intervention_log import InterventionLog

from app.ml.analytics.risk_trend_service import RiskTrendService


class AnalyticsService:

    def get_health_timeline(self, db: Session, user_id: int) -> Dict:

        # =====================================================
        # 1. FETCH HISTORY
        # =====================================================

        history_records = (
            db.query(PredictionHistory)
            .filter(PredictionHistory.user_id == user_id)
            .order_by(PredictionHistory.created_at.asc())
            .all()
        )

        if not history_records:
            legacy_records = (
                db.query(Prediction)
                .filter(Prediction.user_id == user_id)
                .order_by(Prediction.created_at.asc())
                .all()
            )

            timeline = [
                {
                    "created_at": r.created_at,
                    "health_score": r.health_score,
                    "risk_score": r.risk_score,
                    "ai_confidence": r.ai_confidence,
                }
                for r in legacy_records
            ]

            scores = [r.risk_score for r in legacy_records]

        else:
            timeline = [
                {
                    "created_at": r.created_at,
                    "health_score": r.health_score,
                    "risk_score": r.risk_score,
                    "confidence": r.confidence,
                    "predicted_disease": r.predicted_disease,
                    "model_version": r.model_version,
                }
                for r in history_records
            ]

            scores = [r.risk_score for r in history_records]

        # =====================================================
        # 2. RISK TREND ANALYTICS
        # =====================================================

        trend_engine = RiskTrendService()
        risk_trend = trend_engine.compute(scores)

        # =====================================================
        # 3. PERSIST TREND (FIXED - NO DUPLICATES)
        # =====================================================

        if scores:

            latest_record = history_records[-1] if history_records else None

            # check last stored trend to avoid duplicates
            last_trend = (
                db.query(RiskTrend)
                .filter(RiskTrend.user_id == user_id)
                .order_by(RiskTrend.created_at.desc())
                .first()
            )

            is_duplicate = (
                last_trend
                and last_trend.risk_score == scores[-1]
                and last_trend.trend_direction == risk_trend["trend"]
            )

            if not is_duplicate:

                db.add(
                    RiskTrend(
                        user_id=user_id,
                        disease_name=getattr(
                            latest_record,
                            "predicted_disease",
                            "general",
                        ),
                        risk_score=scores[-1],
                        trend_direction=risk_trend["trend"],
                        moving_average_7d=risk_trend["moving_average_7d"],
                        moving_average_30d=risk_trend["moving_average_30d"],
                        volatility_score=risk_trend["volatility_score"],
                    )
                )

        # =====================================================
        # 4. INTERVENTION LOGIC (FIXED DEDUPLICATION)
        # =====================================================

        if scores:

            latest_risk = scores[-1]

            last_intervention = (
                db.query(InterventionLog)
                .filter(InterventionLog.user_id == user_id)
                .order_by(InterventionLog.created_at.desc())
                .first()
            )

            new_intervention = None

            if latest_risk >= 70:
                new_intervention = "alert"

            elif latest_risk < 30:
                new_intervention = "prevention"

            if new_intervention and (
                not last_intervention
                or last_intervention.intervention_type != new_intervention
            ):
                db.add(
                    InterventionLog(
                        user_id=user_id,
                        intervention_type=new_intervention,
                        trigger_source="analytics_engine",
                        description=(
                            "High risk detected - clinical review recommended"
                            if new_intervention == "alert"
                            else "Stable health - maintain lifestyle"
                        ),
                        effectiveness_score=0.0,
                        status="active",
                    )
                )

        # =====================================================
        # 5. COMMIT (CRITICAL FIX)
        # =====================================================

        db.commit()

        # =====================================================
        # 6. RESPONSE
        # =====================================================

        return {
            "user_id": user_id,
            "timeline": timeline,
            "risk_trend": risk_trend,
            "total_records": len(timeline),
        }