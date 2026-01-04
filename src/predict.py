# src/predict.py

import joblib
import pandas as pd
from preprocessing import load_and_preprocess_data

MODEL_PATH = "model/groundwater_model.pkl"
SCALER_PATH = "model/scaler.pkl"


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

    temp_path = "temp_input.csv"
    input_df.to_csv(temp_path, index=False)

    # Preprocess WITHOUT scaling and WITHOUT target
    X, _, _ = load_and_preprocess_data(
        temp_path,
        training=False
    )

    # Load scaler and apply
    scaler = joblib.load(SCALER_PATH)
    X = pd.DataFrame(
        scaler.transform(X),
        columns=X.columns
    )

    # Load trained model
    model = joblib.load(MODEL_PATH)

    prediction = model.predict(X)[0]
    return prediction


if __name__ == "__main__":
    pred = predict_groundwater_level(
        temperature=30,
        rainfall=120,
        ph=7.2,
        dissolved_oxygen=6.5,
        date="2023-08-15"
    )

    print(f"Predicted Groundwater Level: {pred:.3f} meters")
