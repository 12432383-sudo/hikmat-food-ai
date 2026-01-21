import pickle
import numpy as np

# Load the trained model
model = pickle.load(open("food_ai_model.pkl", "rb"))

def analyze_food(barcode, sugar, salt, fat):

    # Create score
    score = sugar + salt + fat
    features = np.array([[sugar, salt, fat, score]])

    prediction = model.predict(features)[0]

    # ---------------------------
    # HEALTH VERDICT
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
        f"**Nutrition breakdown:**\n"
        f"- Sugar: {sugar} g\n"
        f"- Salt: {salt} g\n"
        f"- Saturated Fat: {fat} g\n\n"
        "Your food was analyzed using both nutrition thresholds and AI scoring."
    )

    # ---------------------------
    # SMART SUGGESTIONS
    # ---------------------------
    if prediction == 0:
        suggestions = (
            "• Choose food with less sugar and saturated fat.\n"
            "• Try nuts, yogurt, fruits, or unsweetened alternatives.\n"
            "• Look for labels like 'Low Sodium' or 'No Added Sugar'."
        )
    elif prediction == 1:
        suggestions = (
            "• This food is okay sometimes.\n"
            "• Compare brands and choose the one with lower salt.\n"
            "• Try balancing it with healthy foods during the day."
        )
    else:
        suggestions = (
            "• Good choice! Keep balancing with fruits, vegetables, and water.\n"
        )

    # ---------------------------
    # PLASTIC PACKAGING WARNING
    # ---------------------------
    plastic_warning = (
        "Foods stored in plastic may contain **BPA, phthalates, and microplastics**.\n"
        "These can affect hormones, fertility, and increase cancer risks.\n"
        "Avoid heating plastic containers and choose glass or BPA-free packaging when possible."
    )

    return verdict, explanation, suggestions, plastic_warning
