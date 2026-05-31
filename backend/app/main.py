from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.dashboard import router as dashboard_router
from app.models import user, prediction
from app.api.routes.user import router as user_router
from app.api.routes.insights import router as insights_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.alerts import router as alerts_router

from app.api.routes.prediction import (
    router as prediction_router
)


app = FastAPI(
    title="BehaviorLens AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

app.include_router(
    prediction_router
)