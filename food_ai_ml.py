import joblib
import numpy as np

# Load trained model
model = joblib.load("food_ai_model.pkl")

def predict_health(sugar, salt, sat_fat, calories):
    """
    Predicts whether a food is Healthy or Unhealthy
    using 4 nutritional features.
    """
    features = np.array([[sugar, salt, sat_fat, calories]])
    prediction = model.predict(features)[0]

    return "Healthy" if prediction == 1 else "Unhealthy"
