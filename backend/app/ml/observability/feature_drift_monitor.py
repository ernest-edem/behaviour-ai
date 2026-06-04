from typing import Any, Dict, List
import time


class FeatureDriftMonitor:
    """
    Runtime feature drift monitor.

    Responsibilities:
    - Detect schema drift
    - Track feature payload history
    - Support analytics dashboards
    - Never break prediction flow
    """

    _history: List[Dict[str, Any]] = []

    # ==================================================
    # SCHEMA DRIFT ANALYSIS
    # ==================================================

    @staticmethod
    def analyze(
        incoming: Dict[str, Any],
        expected_schema: Dict[str, float],
    ) -> Dict[str, Any]:

        incoming_keys = set(incoming.keys())
        expected_keys = set(expected_schema.keys())

        missing = sorted(
            list(expected_keys - incoming_keys)
        )

        extra = sorted(
            list(incoming_keys - expected_keys)
        )

        return {
            "timestamp": time.time(),
            "missing_features": missing,
            "extra_features": extra,
            "feature_count": len(incoming),
            "schema_count": len(expected_schema),
            "drift_detected": bool(
                missing or extra
            ),
        }

    # ==================================================
    # FEATURE RECORDING
    # ==================================================

    @classmethod
    def record(
        cls,
        feature_vector: Dict[str, Any],
    ) -> None:
        """
        Shadow-safe monitoring.

        Never raises.
        """

        try:

            cls._history.append(
                {
                    "timestamp": time.time(),
                    "feature_count": len(
                        feature_vector
                    ),
                    "features": dict(
                        feature_vector
                    ),
                }
            )

            # Prevent memory growth
            if len(cls._history) > 1000:
                cls._history = cls._history[-500:]

        except Exception:
            pass

    # ==================================================
    # HISTORY
    # ==================================================

    @classmethod
    def get_history(
        cls,
    ) -> List[Dict[str, Any]]:

        return list(cls._history)

    @classmethod
    def clear(
        cls,
    ) -> None:

        cls._history.clear()

    @classmethod
    def count(
        cls,
    ) -> int:

        return len(cls._history)

    # ==================================================
    # DEBUG
    # ==================================================

    @classmethod
    def summary(
        cls,
    ) -> Dict[str, Any]:

        return {
            "records": len(cls._history),
            "monitoring_enabled": True,
        }