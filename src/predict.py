# src/predict.py

import joblib
import pandas as pd
from preprocessing import load_and_preprocess_data

MODEL_PATH = "model/groundwater_model.pkl"


def predict_groundwater_level(
    temperature,
    rainfall,
    ph,
    dissolved_oxygen,
    date
):
    """
    Predict groundwater level for given environmental conditions.
    """

    # Create a single-row DataFrame (same structure as training data)
    input_df = pd.DataFrame({
        "Date": [date],
        "Temperature_C": [temperature],
        "Rainfall_mm": [rainfall],
        "pH": [ph],
        "Dissolved_Oxygen_mg_L": [dissolved_oxygen]
    })

    # Save temporarily to reuse preprocessing logic
    temp_path = "temp_input.csv"
    input_df.to_csv(temp_path, index=False)

    # Apply preprocessing
    X, _, _ = load_and_preprocess_data(temp_path)

    # Load trained model
    model = joblib.load(MODEL_PATH)

    # Predict groundwater level
    prediction = model.predict(X)[0]

    return prediction
