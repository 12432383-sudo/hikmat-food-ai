import streamlit as st
import requests
from food_ai_ml import predict_health
from health_insights import explain_prediction

st.set_page_config(page_title="Hikmat Food AI", page_icon="🥗", layout="centered")

st.title("🥗 Hikmat Food AI")
st.write("Scan or enter a barcode to understand how healthy a product really is.")

# -------------------------------------------------------
# Fetch product from OpenFoodFacts
# -------------------------------------------------------
def fetch_product(barcode):
    try:
        url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        res = requests.get(url, timeout=10).json()

        if res.get("status") != 1:
            return None
        return res["product"]
    except Exception as e:
        st.error(f"API error: {e}")
        return None

# -------------------------------------------------------
# Palm oil detection
# -------------------------------------------------------
def detect_palm_oil(ingredients_text):
    if not ingredients_text:
        return 0

    text = ingredients_text.lower()
    triggers = ["palm oil", "huile de palme", "palmiste", "palmitate"]

    return 1 if any(word in text for word in triggers) else 0

# -------------------------------------------------------
# UI
# -------------------------------------------------------
barcode = st.text_input("Enter product barcode")

if st.button("Analyze Food"):
    product = fetch_product(barcode)

    if not product:
        st.error("❌ Product not found in OpenFoodFacts")
    else:
        name = product.get("product_name", "Unknown")
        st.subheader(f"📦 {name}")

        # Extract nutrition
        nutriments = product.get("nutriments", {})
        sugar = nutriments.get("sugars_100g", 0)
        salt = nutriments.get("salt_100g", 0)
        sat_fat = nutriments.get("saturated-fat_100g", 0)
        ingredients = product.get("ingredients_text", "")

        # Palm oil detection
        palm_oil = detect_palm_oil(ingredients)

        st.write("### 🔬 Nutrition (per 100g)")
        st.write(f"- Sugar: **{sugar} g**")
        st.write(f"- Salt: **{salt} g**")
        st.write(f"- Saturated Fat: **{sat_fat} g**")
        st.write(f"- Palm Oil: **{'Yes' if palm_oil else 'No'}**")

        # ML Prediction
        verdict = predict_health(sugar, salt, sat_fat, palm_oil)

        # -------------------------------------------------------
        # AI Verdict (fixed clean version)
        # -------------------------------------------------------
        st.write("### 🤖 AI Verdict")

        if verdict == "healthy":
            st.success("Healthy ✔")
        elif verdict == "moderate":
            st.warning("Moderate ⚠️")
        elif verdict == "unhealthy":
            st.error("Unhealthy ❌")
        elif verdict == "very unhealthy":
            st.error("Very Unhealthy ❌🔥")
        else:
            st.error(verdict)

        # Human explanations
        reasons, advice = explain_prediction(verdict, sugar, salt, sat_fat, palm_oil)

        st.write("### 📌 Why this verdict?")
        st.write(reasons)

        st.write("### ⭐ Better Choices")
        st.write(advice)
