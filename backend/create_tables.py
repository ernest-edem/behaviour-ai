from app.database.db import engine, Base

from app.models.user import User
from app.models.prediction import Prediction
from app.models.prediction_symptom import PredictionSymptom
from app.models.lifestyle_log import LifestyleLog
from app.models.symptom_log import SymptomLog
from app.models.health_report import HealthReport
from app.models.disease_risk_history import DiseaseRiskHistory

Base.metadata.create_all(bind=engine)

print("Tables created successfully")