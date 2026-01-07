import streamlit as st
import requests
from food_ai_ml import predict_health
from explain_ai import explain_like_human


# -----------------------------
# Fetch product from OpenFoodFacts (SAFE)
# -----------------------------
def get_product(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = requests.get(url, timeout=8)
        data = response.json()

        if data.get("status") != 1:
            return None, "not_found"

        return data.get("product", {}), None

    except requests.exceptions.Timeout:
        return None, "timeout"
    except Exception as e:
        return None, str(e)


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="Hikmat Food AI",
    page_icon="🥗",
    layout="centered"
)

st.title("🥗 Hikmat Food AI")
st.write(
    "Scan or enter a barcode to understand **how healthy a product really is**.\n\n"
    "If the product cannot be found, you can still analyze it manually."
)

barcode = st.text_input("📦 Enter product barcode", placeholder="e.g. 3017620422003")

product = None
error_type = None

if barcode:
    product, error_type = get_product(barcode)

    if error_type == "timeout":
        st.warning(
            "⚠️ The food database is currently slow or unavailable.\n\n"
            "You can still analyze the product by entering nutrition values manually."
        )

    elif error_type == "not_found":
        st.info(
            "ℹ️ This product was not found in the database.\n\n"
            "You can still analyze it manually."
        )

# -----------------------------
# Manual or API nutrition input
# -----------------------------
st.subheader("🔬 Nutrition per 100g")

if product:
    nutriments = product.get("nutriments", {})
    product_name = product.get("product_name", "Unknown product")

    sugar = nutriments.get("sugars_100g", 0.0)
    salt = nutriments.get("salt_100g", 0.0)
    sat_fat = nutriments.get("saturated-fat_100g", 0.0)
    calories = nutriments.get("energy-kcal_100g", 0.0)

    st.subheader(f"📦 {product_name}")

else:
    sugar = st.number_input("🍬 Sugar (g)", min_value=0.0, value=10.0)
    salt = st.number_input("🧂 Salt (g)", min_value=0.0, value=0.5)
    sat_fat = st.number_input("🧈 Saturated fat (g)", min_value=0.0, value=3.0)
    calories = st.number_input("🔥 Calories (kcal)", min_value=0.0, value=250.0)

if st.button("Analyze Food"):
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

    st.caption("ℹ️ Educational use only — not medical advice.")
