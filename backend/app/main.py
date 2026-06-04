import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.user import router as user_router
from app.api.routes.insights import router as insights_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.alerts import router as alerts_router
from app.api.routes.prediction import router as prediction_router
from app.api.routes.explainability import router as explainability_router

from app.models import user, prediction  # noqa: F401

from app.ml.registry.model_registry import model_registry


app = FastAPI(
    title="BehaviorLens AI",
    version="1.0.0"
)

# =====================================
# CORS
# =====================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================
# HEALTH CHECK
# =====================================
@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "BehaviorLens AI API running"
    }


# =====================================
# ROUTERS
# =====================================
app.include_router(user_router)
app.include_router(dashboard_router)
app.include_router(insights_router)
app.include_router(analytics_router)
app.include_router(alerts_router)
app.include_router(prediction_router)
app.include_router(explainability_router)


# =====================================
# STARTUP — MODEL REGISTRY BOOTSTRAP
# =====================================
@app.on_event("startup")
def load_ml_models() -> None:
    """
    Load and register ML model safely.
    System MUST run even without model (shadow mode supported).
    """

    try:
        from app.ml.adapters.sklearn_adapter import SklearnAdapter
    except Exception as exc:
        print(f"[STARTUP ERROR] Adapter import failed: {exc}", file=sys.stderr)
        return

    model_path = Path(__file__).resolve().parent.parent / "models" / "model.pkl"

    if not model_path.exists():
        print(
            f"[STARTUP WARNING] Model not found at {model_path}. "
            "Running in RULE_ENGINE + SHADOW ML mode.",
            file=sys.stderr,
        )
        return

    try:
        adapter = SklearnAdapter(
            model_name="behavior_model",
            version="1.0.0",
        )

        adapter.load_model(str(model_path))

        model_registry.register(
            name="behavior_model",
            model=adapter,
            version="1.0.0",
        )

        model_registry.set_active_model("behavior_model")

        print(
            "[STARTUP] ML model registered successfully: behavior_model v1.0.0",
            file=sys.stderr,
        )

    except Exception as exc:
        print(
            f"[STARTUP ERROR] Failed to load ML model: {exc}. "
            "Continuing in shadow mode.",
            file=sys.stderr,
        )