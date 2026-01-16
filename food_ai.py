import joblib
import numpy as np

model = joblib.load("food_ai_model.pkl")

def predict_health(sugar, salt, sat_fat, palm_oil):
    features = np.array([[sugar, salt, sat_fat, palm_oil]])
    prediction = model.predict(features)[0]
    return prediction
