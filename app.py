import streamlit as st
import requests
import joblib

# Load ML model
model = joblib.load("food_ai_model.pkl")

LABELS = {
    0: "Healthy ✅",
    1: "Moderate ⚠️",
    2: "Unhealthy ❌"
}

# Fetch product
def get_product(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if data.get("status") != 1:
            return None
        return data["product"]
    except:
        return None

# Extract features
def extract_features(product):
    nutriments = product.get("nutriments", {})

    sugar = nutriments.get("sugars_100g", 0)
    salt = nutriments.get("salt_100g", 0)
    sat_fat = nutriments.get("saturated-fat_100g", 0)

    ingredients = (
        product.get("ingredients_text", "")
        + product.get("ingredients_text_en", "")
    ).lower()

    palm_oil = 1 if "palm oil" in ingredients else 0

    return [[sugar, salt, sat_fat, palm_oil]]

# ---------------- UI ----------------

st.set_page_config(page_title="Hikmat Food AI", page_icon="🥗")

st.title("🥗 Hikmat Food AI")
st.write("Scan or enter a barcode to check how healthy a product is.")

barcode = st.text_input("📦 Enter barcode")

if st.button("Analyze"):
    product = get_product(barcode)

    if not product:
        st.error("❌ Product not found")
    else:
        name = product.get("product_name", "Unknown product")
        features = extract_features(product)
        prediction = model.predict(features)[0]

        st.subheader(f"📦 {name}")
        st.success(f"🤖 AI Verdict: {LABELS[prediction]}")

        st.write("### 🔬 Nutrition per 100g")
        nutriments = product.get("nutriments", {})
        st.write("Sugar:", nutriments.get("sugars_100g", "N/A"))
        st.write("Salt:", nutriments.get("salt_100g", "N/A"))
        st.write("Saturated fat:", nutriments.get("saturated-fat_100g", "N/A"))
