import streamlit as st
import pandas as pd
from analyze import analyze_food

st.set_page_config(page_title="Hikmat Food AI", layout="wide")

st.title("🥗 Hikmat Food AI")
st.write(
    "Scan a food barcode or enter nutrition values manually. "
    "The AI explains health risks, plastic dangers, and better alternatives."
)

# -----------------------
# SESSION HISTORY
# -----------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------
# CAMERA INPUT (SUPPORTED)
# -----------------------
st.subheader("📷 Scan Barcode (Photo)")
image = st.camera_input("Open camera and take a picture of the barcode")

if image:
    st.success(
        "Photo captured ✅\n\n"
        "⚠️ Live barcode decoding will be added next.\n"
        "For now, enter the barcode manually below."
    )

# -----------------------
# BARCODE INPUT
# -----------------------
barcode = st.text_input("Barcode (numbers only)")

# -----------------------
# NUTRITION INPUTS
# -----------------------
st.subheader("🧪 Nutrition per 100g")
sugar = st.number_input("Sugar (g)", 0.0, 200.0, step=0.1)
salt = st.number_input("Salt (g)", 0.0, 50.0, step=0.1)
fat = st.number_input("Saturated Fat (g)", 0.0, 100.0, step=0.1)

# -----------------------
# ANALYSIS
# -----------------------
if st.button("🔍 Analyze Food"):
    verdict, explanation, suggestions, plastic_warning = analyze_food(
        barcode, sugar, salt, fat
    )

    st.subheader("🤖 AI Verdict")
    st.info(verdict)

    st.subheader("🧠 Explanation")
    st.markdown(explanation)

    st.subheader("🥦 Healthier Alternatives")
    st.markdown(suggestions)

    st.subheader("⚠️ Plastic & Packaging Warning")
    st.warning(plastic_warning)

    st.session_state.history.append({
        "Barcode": barcode,
        "Sugar": sugar,
        "Salt": salt,
        "Fat": fat,
        "Verdict": verdict
    })

# -----------------------
# HISTORY
# -----------------------
st.subheader("📜 Scan History")
if st.session_state.history:
    st.dataframe(pd.DataFrame(st.session_state.history))
else:
    st.write("No scans yet.")
