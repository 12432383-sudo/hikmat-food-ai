import joblib
import numpy as np

# Load trained ML model
model = joblib.load("food_ai_model.pkl")

# --------------------------------------------------
# ML Prediction (FIXED: 4 FEATURES)
# --------------------------------------------------
def predict_health(sugar, salt, sat_fat, calories):
    features = np.array([[sugar, salt, sat_fat, calories]])
    prediction = model.predict(features)[0]
    return "Healthy" if prediction == 1 else "Unhealthy"


# --------------------------------------------------
# Human-like Explanation Engine
# --------------------------------------------------
def explain_verdict(sugar, salt, sat_fat, calories, verdict):
    reasons = []
    suggestions = []

    if sugar > 10:
        reasons.append("it contains a high amount of sugar, which may cause energy crashes and weight gain")
        suggestions.append("choose foods with natural sugars like fruits")

    if sat_fat > 5:
        reasons.append("it is high in saturated fat, which can increase heart disease risk")
        suggestions.append("prefer foods with healthy fats like nuts, avocado, or olive oil")

    if salt > 1.2:
        reasons.append("it has a lot of salt, which may increase blood pressure")
        suggestions.append("look for low-salt or lightly seasoned alternatives")

    if calories > 400:
        reasons.append("it is calorie-dense, so frequent consumption may lead to weight gain")
        suggestions.append("consume smaller portions or lighter snacks")

    if verdict == "Unhealthy" and reasons:
        explanation = (
            "This product is considered unhealthy because "
            + ", and ".join(reasons)
            + "."
        )
    else:
        explanation = (
            "This product appears relatively healthy. Still, balanced consumption is recommended."
        )

    suggestions = list(set(suggestions))  # remove duplicates
    return explanation, suggestions
