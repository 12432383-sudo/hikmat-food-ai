import joblib
import numpy as np

model = joblib.load("food_ai_model.pkl")

def predict_health(sugar, salt, sat_fat, calories):
    features = np.array([[sugar, salt, sat_fat, calories]])
    prediction = model.predict(features)[0]
    return "Healthy" if prediction == 1 else "Unhealthy"
