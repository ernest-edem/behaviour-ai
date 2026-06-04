"""Quick integration test for the FeatureBuilder and orchestrator chain."""

from pydantic import BaseModel
from typing import List
import json

from app.ml.features.feature_builder import FeatureBuilder


class FakeRequest(BaseModel):
    sleep_hours: float = 5.0
    exercise_minutes: int = 15
    water_intake_liters: float = 1.0
    stress_level: int = 8
    screen_time_hours: float = 10.0
    smoker: bool = True
    alcohol_use: bool = False
    diet_quality: int = 3
    fruits_per_day: int = 1
    vegetables_per_day: int = 1
    symptoms: List[str] = ["fatigue", "chest pain"]


def test_feature_builder():
    req = FakeRequest()
    vec = FeatureBuilder.build(req)
    print("=== FeatureBuilder.build() ===")
    print(json.dumps(vec, indent=2))
    print(f"Keys count: {len(vec)}")
    assert len(vec) == 10, f"Expected 10 features, got {len(vec)}"
    assert all(isinstance(v, float) for v in vec.values()), "All values must be float"
    assert vec["smoker"] == 1.0, "smoker=True should be 1.0"
    assert vec["alcohol_use"] == 0.0, "alcohol_use=False should be 0.0"
    print("✓ All assertions passed\n")


def test_feature_builder_with_none():
    """Test that None values get safe defaults."""
    vec = FeatureBuilder.build({})
    print("=== FeatureBuilder.build({}) — all defaults ===")
    print(json.dumps(vec, indent=2))
    assert len(vec) == 10
    assert all(v > 0 or v == 0.0 for v in vec.values()), "Defaults must be non-negative"
    print("✓ All assertions passed\n")


def test_data_cleaner():
    from app.ml.preprocessing.data_cleaner import DataCleaner
    cleaner = DataCleaner()

    # Pass-through for Pydantic model
    req = FakeRequest()
    result = cleaner.clean(req)
    assert result is req, "Non-DataFrame should pass through"
    print("=== DataCleaner.clean(pydantic) ===")
    print("✓ Pass-through works\n")


def test_orchestrator_import():
    """Ensure the orchestrator imports without error."""
    from app.ml.inference.prediction_orchestrator import PredictionOrchestrator
    orch = PredictionOrchestrator()
    print("=== PredictionOrchestrator ===")
    print(f"✓ Instantiated successfully: {orch}")
    print()


def test_pipeline_import():
    """Ensure the pipeline imports without error."""
    from app.ml.inference.prediction_pipeline import PredictionPipeline
    pipe = PredictionPipeline()
    print("=== PredictionPipeline ===")
    print(f"✓ Instantiated successfully: {pipe}")
    print()


def test_explainability_route_import():
    """Ensure the explainability router imports without error."""
    from app.api.routes.explainability import router
    print("=== Explainability Router ===")
    print(f"✓ Imported: {router}")
    print()


def test_main_import():
    """Ensure main.py imports without error."""
    from app.main import app
    routes = [r.path for r in app.routes]
    print("=== FastAPI app ===")
    print(f"Routes: {routes}")
    has_explainability = any("/explainability" in r for r in routes)
    assert has_explainability, "Explainability route not registered!"
    print("✓ Explainability route is registered")
    print()


if __name__ == "__main__":
    test_feature_builder()
    test_feature_builder_with_none()
    test_data_cleaner()
    test_orchestrator_import()
    test_pipeline_import()
    test_explainability_route_import()
    test_main_import()
    print("=" * 50)
    print("ALL TESTS PASSED")
    print("=" * 50)
