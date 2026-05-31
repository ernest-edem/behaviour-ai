import joblib
import os

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "model.pkl"
)

ENCODER_PATH = os.path.join(
    os.path.dirname(__file__),
    "label_encoder.pkl"
)

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)


def predict_disease(features):
    prediction = model.predict(features)[0]

    disease = label_encoder.inverse_transform(
        [prediction]
    )[0]

    probabilities = model.predict_proba(features)[0]

    confidence = round(
        max(probabilities) * 100,
        2
    )

    return {
        "disease": disease,
        "confidence": confidence,
        "probabilities": probabilities.tolist()
    }


def get_feature_importance():
    return model.feature_importances_