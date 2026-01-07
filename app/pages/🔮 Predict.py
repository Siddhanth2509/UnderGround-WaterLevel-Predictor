import sys
import os

# ---------- PATH FIX (MUST BE FIRST) ----------
ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
# ---------------------------------------------

import streamlit as st
from src.predict import predict_groundwater_level

st.title("🔮 Groundwater Prediction")

temperature = st.number_input("Temperature (°C)", value=25.0)
rainfall = st.number_input("Rainfall (mm)", value=100.0)
ph = st.slider("pH", 0.0, 14.0, 7.0)
dissolved_oxygen = st.number_input("Dissolved Oxygen (mg/L)", value=6.0)
date = st.date_input("Date")

if st.button("Predict"):
    prediction = predict_groundwater_level(
        temperature,
        rainfall,
        ph,
        dissolved_oxygen,
        date
    )
    st.success(f"Predicted Groundwater Level: {prediction:.2f} m")
