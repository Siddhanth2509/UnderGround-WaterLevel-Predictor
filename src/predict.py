import os
import joblib
import pandas as pd

from src.preprocessing import load_and_preprocess_data

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "groundwater_model.pkl")

model = joblib.load(MODEL_PATH)

def predict_groundwater_level(
    temperature,
    rainfall,
    ph,
    dissolved_oxygen,
    date
):
    input_df = pd.DataFrame({
        "Date": [date],
        "Temperature_C": [temperature],
        "Rainfall_mm": [rainfall],
        "pH": [ph],
        "Dissolved_Oxygen_mg_L": [dissolved_oxygen]
    })

    X_scaled, _, _ = load_and_preprocess_data(
        input_df,
        training=False
    )

    return float(model.predict(X_scaled)[0])
