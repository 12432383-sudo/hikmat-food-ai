import streamlit as st
import json
import pandas as pd
import base64
from analyze import analyze_food

import streamlit.components.v1 as components

st.set_page_config(page_title="Hikmat Food AI", layout="wide")

st.title("🥗 Hikmat Food AI")
st.write("Scan a barcode or enter it manually. The AI will analyze nutrition, packaging risks, and suggest healthier alternatives.")

# -----------------------
# SESSION HISTORY STORAGE
# -----------------------
if "history" not in st.session_state:
    st.session_state["history"] = []

# -----------------------
# REAL-TIME BARCODE SCANNER (JS + QuaggaJS)
# -----------------------

html_code = """
<!DOCTYPE html>
<html>
  <body style="margin:0; padding:0; text-align:center;">

    <video id="video" width="350" height="250" autoplay style="border-radius: 10px;"></video>
    <p id="result" style="font-size:20px;"></p>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/quagga/0.12.1/quagga.min.js"></script>

    <script>
      function startScanner(){
        Quagga.init({
          inputStream: {
            name: "Live",
            type: "LiveStream",
            target: document.querySelector('#video'),
          },
          decoder: { readers: ["ean_reader", "ean_13_reader", "upc_reader", "code_128_reader"] }
        }, function(err){
          if(err){ console.log(err); return }
          Quagga.start();
        });

        Quagga.onDetected(function(data){
          const code = data.codeResult.code;
          document.getElementById("result").innerHTML = "Scanned: " + code;

          // Send barcode to Streamlit
          window.parent.postMessage({barcode: code}, "*");
        });
      }

      startScanner();
    </script>
  </body>
</html>
"""

components.html(html_code, height=350)

barcode = st.text_input("Barcode (auto-filled if scanned)")

# -----------------------
# USER INPUTS
# -----------------------
st.subheader("Nutrition Info")
sugar = st.number_input("Sugar (g)", min_value=0.0, max_value=200.0, step=0.1)
salt = st.number_input("Salt (g)", min_value=0.0, max_value=200.0, step=0.1)
fat = st.number_input("Saturated Fat (g)", min_value=0.0, max_value=200.0, step=0.1)

# -----------------------
# PROCESS ANALYSIS
# -----------------------
if st.button("🔍 Analyze Food"):
    verdict, explanation, suggestions, plastic_warning = analyze_food(
        barcode, sugar, salt, fat
    )

    st.subheader("AI Verdict")
    st.info(verdict)

    st.subheader("Explanation")
    st.write(explanation)

    st.subheader("Better Choices / Healthier Alternatives")
    st.write(suggestions)

    st.subheader("Packaging & Plastic Safety Warning")
    st.warning(plastic_warning)

    # Save history
    st.session_state["history"].append({
        "barcode": barcode,
        "sugar": sugar,
        "salt": salt,
        "fat": fat,
        "verdict": verdict
    })

# -----------------------
# HISTORY SECTION
# -----------------------
st.subheader("📜 Scan History")
if len(st.session_state["history"]) > 0:
    st.dataframe(pd.DataFrame(st.session_state["history"]))
else:
    st.write("No scans yet.")
