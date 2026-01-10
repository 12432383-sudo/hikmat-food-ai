import streamlit as st
import requests
import cv2
import numpy as np
from pyzbar.pyzbar import decode

from food_ai_ml import predict_health
from explain_ai import explain_like_human
from health_insights import packaging_insights, additive_insights, ultra_processed_insights


# -----------------------------
# Decode barcode from image
# -----------------------------
def decode_barcode(image_bytes):
    np_img = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    detected = decode(img)

    if detected:
        return detected[0].data.decode("utf-8")  # return barcode
    return None


# -----------------------------
# Fetch product
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
st.set_page_config(page_title="Hikmat Food AI", page_icon="🥗", layout="centered")

st.title("🥗 Hikmat Food AI")
st.write("Scan or enter a barcode to understand **how healthy a product really is**.")


# -----------------------------
# BARCODE SCANNER SECTION
# -----------------------------
st.subheader("📷 Barcode Scanner (Phone Camera)")

img = st.camera_input("Tap to scan barcode")

barcode = None

if img:
    st.info("🔄 Scanning image for barcode...")
    barcode = decode_barcode(img.getvalue())

    if barcode:
        st.success(f"✅ Barcode detected: **{barcode}**")
    else:
        st.error("❌ Could not detect a barcode. Try again.")


# -----------------------------
# MANUAL BARCODE INPUT
# -----------------------------
st.subheader("🔢 Or enter barcode manually")

barcode_manual = st.text_input("Enter barcode")

if barcode_manual.strip():
    barcode = barcode_manual.strip()


# -----------------------------
# Fetch product and nutrition
# -----------------------------
product = None
error_type = None

if barcode:
    product, error_type = get_product(barcode)

    if error_type == "timeout":
        st.warning("⚠️ OpenFoodFacts API timeout. You can still enter nutrition manually.")

    elif error_type == "not_found":
        st.warning("ℹ️ Product not found. Please enter nutrition manually.")


st.subheader("🔬 Nutrition per 100g")

if product:
    nutrients = product.get("nutriments", {})
    product_name = product.get("product_name", "Unknown product")

    st.subheader(f"📦 {product_name}")

    sugar = nutrients.get("sugars_100g", 0.0)
    salt = nutrients.get("salt_100g", 0.0)
    sat_fat = nutrients.get("saturated-fat_100g", 0.0)
    calories = nutrients.get("energy-kcal_100g", 0.0)
else:
    sugar = st.number_input("🍬 Sugar (g)", min_value=0.0, value=10.0)
    salt = st.number_input("🧂 Salt (g)", min_value=0.0, value=0.5)
    sat_fat = st.number_input("🧈 Saturated fat (g)", min_value=0.0, value=3.0)
    calories = st.number_input("🔥 Calories (kcal)", min_value=0.0, value=250.0)


# -----------------------------
# Button to analyze
# -----------------------------
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

    for r in reasons:
        st.warning(r)

    for a in advice:
        st.success(a)

    # Packaging analysis
    if product:
        p_warnings = packaging_insights(product)
        if p_warnings:
            st.subheader("🚨 Packaging Warnings")
            for w in p_warnings:
                st.error(w)

        # Additives
        add_warnings = additive_insights(product)
        if add_warnings:
            st.subheader("⚗️ Additives")
            for w in add_warnings:
                st.warning(w)

        # Ultra-processed
        ultra = ultra_processed_insights(product)
        if ultra:
            st.subheader("🍔 Ultra-Processed Food")
            for w in ultra:
                st.error(w)

st.caption("Built by Hikmat — making food smarter 🧠")
