import streamlit as st
import requests

from food_ai_ml import predict_health
from explain_ai import explain_like_human


# -----------------------------
# Fetch product from OpenFoodFacts
# -----------------------------
def get_product(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("status") != 1:
            return None
        return data.get("product", {})
    except Exception as e:
        st.error(f"API error: {e}")
        return None


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="Hikmat Food AI",
    page_icon="🥗",
    layout="centered"
)

st.title("🥗 Hikmat Food AI")
st.write("Scan or enter a barcode to understand **how healthy a product really is**.")

barcode = st.text_input("📦 Enter product barcode", placeholder="e.g. 3017620422003")

if barcode:
    product = get_product(barcode)

    if not product:
        st.error("❌ Product not found in OpenFoodFacts")
    else:
        nutriments = product.get("nutriments", {})

        product_name = product.get("product_name", "Unknown product")

        sugar = nutriments.get("sugars_100g", 0.0)
        salt = nutriments.get("salt_100g", 0.0)
        sat_fat = nutriments.get("saturated-fat_100g", 0.0)
        calories = nutriments.get("energy-kcal_100g", 0.0)

        st.subheader(f"📦 {product_name}")

        st.write("### 🔬 Nutrition per 100g")
        st.write(f"- 🍬 Sugar: **{sugar} g**")
        st.write(f"- 🧂 Salt: **{salt} g**")
        st.write(f"- 🧈 Saturated fat: **{sat_fat} g**")
        st.write(f"- 🔥 Calories: **{calories} kcal**")

        verdict = predict_health(sugar, salt, sat_fat, calories)

        st.subheader("🤖 AI Verdict")
        if verdict == "Unhealthy":
            st.error("Unhealthy ❌")
        else:
            st.success("Healthy ✅")

        tone, reasons, advice = explain_like_human(
            verdict, sugar, salt, sat_fat, calories
        )

        st.subheader("🧠 AI Explanation")
        st.write(tone)

        if reasons:
            st.subheader("⚠️ Why?")
            for r in reasons:
                st.warning(r)

        if advice:
            st.subheader("🥗 Better choices")
            for a in advice:
                st.success(a)

        st.caption("ℹ️ This AI provides educational insights, not medical advice.")
