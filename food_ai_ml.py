import pickle
import numpy as np

model = pickle.load(open("food_ai_model.pkl", "rb"))

def analyze_food(barcode, sugar, salt, fat):

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
        f"- Sugar: {sugar}g\n"
        f"- Salt: {salt}g\n"
        f"- Saturated Fat: {fat}g\n\n"
        f"Your food was analyzed based on known health thresholds.\n"
    )

    # ---------------------------
    # SMART SUGGESTIONS
    # ---------------------------
    if prediction == 0:
        suggestions = (
            "• Try choosing a low-sugar & low-fat alternative.\n"
            "• Check for labels like 'Low Sodium', 'Light', or 'No Added Sugar'.\n"
            "• Prefer whole foods like nuts, yogurt, fruit, or water-based drinks.\n"
        )
    elif prediction == 1:
        suggestions = (
            "• This food is okay occasionally.\n"
            "• Look for a low-sodium or low-fat version.\n"
            "• Try mixing with healthier options to balance it.\n"
        )
    else:
        suggestions = (
            "• Great choice! Balanced nutrients.\n"
            "• Add vegetables, fruits, and water for a fully healthy routine.\n"
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


