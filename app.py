import streamlit as st
from food_ai_ml import predict_health
import joblib

# Load ML model (already trained)
model = joblib.load("food_ai_model.pkl")

# ---------- HUMAN EXPLANATION FUNCTION ----------
def explain_like_human(sugar, salt, sat_fat, verdict):
    explanation = ""

    if verdict == "Unhealthy":
        explanation += "This product is considered unhealthy mainly because of its nutritional balance. "

        if sugar > 10:
            explanation += f"It contains a high amount of sugar ({sugar}g per 100g), which can increase the risk of weight gain and diabetes if consumed often. "

        if salt > 1:
            explanation += f"The salt level is quite high ({salt}g per 100g), which may negatively affect blood pressure. "

        if sat_fat > 5:
            explanation += f"It also has a high level of saturated fat ({sat_fat}g per 100g), which is not good for heart health. "

        explanation += "Eating this occasionally is okay, but it should not be a daily habit."

        suggestion = (
            "Try choosing foods with less sugar, lower salt, and healthier fats. "
            "Examples include plain yogurt, nuts, fruits, oats, or homemade snacks."
        )

    else:
        explanation += "This product has a relatively balanced nutritional profile. "

        if sugar <= 10:
            explanation += "Its sugar content is moderate. "

        if salt <= 1:
            explanation += "The salt level is within a safe range. "

        if sat_fat <= 5:
            explanation += "Saturated fat is not excessive. "

        explanation += "This makes it a reasonable choice when eaten in moderation."

        suggestion = (
            "You can include this food in a balanced diet. "
            "Still, variety is important, so mix it with fresh and whole foods."
        )

    return explanation, suggestion


# ---------- STREAMLIT UI ----------
st.set_page_config(page_title="Hikmat Food AI", page_icon="🥗")

st.title("🥗 Hikmat Food AI")
st.write("Scan or enter a food barcode to understand how healthy it is — explained like a human.")

barcode = st.text_input("📦 Enter product barcode (numbers only):")

if barcode:
    # Demo nutrition values (later replaced by real API data)
    sugar = st.number_input("Sugar (g per 100g)", value=10.0)
    salt = st.number_input("Salt (g per 100g)", value=0.5)
    sat_fat = st.number_input("Saturated fat (g per 100g)", value=3.0)

    if st.button("Analyze Food"):
        verdict = predict_health(sugar, salt, sat_fat)

        st.subheader("🤖 AI Verdict")
        if verdict == "Unhealthy":
            st.error("Unhealthy ❌")
        else:
            st.success("Healthy ✅")

        explanation, suggestion = explain_like_human(
            sugar, salt, sat_fat, verdict
        )

        st.subheader("🧠 AI Explanation")
        st.write(explanation)

        st.subheader("🥦 Healthier Advice")
        st.info(suggestion)

        st.caption("⚠️ This AI provides educational insights, not medical advice.")
