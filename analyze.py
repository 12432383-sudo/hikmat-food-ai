import joblib
import numpy as np

# ---------------------------
# LOAD MODEL (JOBLIB ONLY)
# ---------------------------
model = joblib.load("food_ai_model.pkl")

def analyze_food(barcode, sugar, salt, fat):
    # ---------------------------
    # FEATURE ENGINEERING
    # ---------------------------
    score = sugar + salt + fat
    features = np.array([[sugar, salt, fat, score]])

    prediction = model.predict(features)[0]

    # ---------------------------
    # AI VERDICT
    # ---------------------------
    if prediction == 0:
        verdict = "❌ Unhealthy"
    elif prediction == 1:
        verdict = "⚠️ Moderate"
    else:
        verdict = "✅ Healthy"

    # ---------------------------
    # HUMAN EXPLANATION
    # ---------------------------
    explanation = (
        f"This food contains **{sugar}g sugar**, **{salt}g salt**, "
        f"and **{fat}g saturated fat per 100g**.\n\n"
        "The AI combined these values using nutrition science and "
        "machine-learning patterns learned from real food data."
    )

    # ---------------------------
    # SMART SUGGESTIONS
    # ---------------------------
    if prediction == 0:
        suggestions = (
            "• Reduce sugar and saturated fat intake.\n"
            "• Choose whole foods like fruits, yogurt, nuts.\n"
            "• Avoid ultra-processed snacks and sugary drinks."
        )
    elif prediction == 1:
        suggestions = (
            "• Acceptable occasionally.\n"
            "• Balance your day with vegetables and water.\n"
            "• Prefer lower-salt alternatives."
        )
    else:
        suggestions = (
            "• Excellent choice!\n"
            "• Keep combining with fresh, unprocessed foods."
        )

    # ---------------------------
    # PLASTIC WARNING
    # ---------------------------
    plastic_warning = (
        "⚠️ **Plastic Risk**\n\n"
        "Food packaging made of plastic may release BPA and microplastics, "
        "especially when heated.\n"
        "Prefer glass or paper packaging when possible."
    )

    return verdict, explanation, suggestions, plastic_warning
