from enum import Enum


class PhenotypeType(str, Enum):
    BURNOUT_PRONE = "Burnout-Prone"
    EMOTIONALLY_OVERWHELMED = "Emotionally Overwhelmed"
    DISTRESSED_NON_ADHERENT = "Distressed Non-Adherent"
    HIGH_CARDIOMETABOLIC_RISK = "High Cardiometabolic Risk"
    PREVENTION_OPPORTUNITY = "Prevention Opportunity"
    STABLE_HEALTHY = "Stable Healthy"