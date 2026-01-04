# src/preprocessing.py

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

def load_and_preprocess_data(csv_path, scale_for_linear=False):

    df = pd.read_csv(csv_path)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.sort_values("Date").reset_index(drop=True)
    df = df.dropna(subset=["Date"])

    df["Month"] = df["Date"].dt.month
    df["DayOfYear"] = df["Date"].dt.dayofyear

    feature_cols = [
        "Temperature_C",
        "Rainfall_mm",
        "pH",
        "Dissolved_Oxygen_mg_L",
        "Month",
        "DayOfYear"
    ]

    target_col = "Water_Level_m"

    X = df[feature_cols]
    y = df[target_col]

    imputer = SimpleImputer(strategy="median")
    X = pd.DataFrame(imputer.fit_transform(X), columns=feature_cols)

    scaler = None
    if scale_for_linear:
        scaler = StandardScaler()
        X = pd.DataFrame(scaler.fit_transform(X), columns=feature_cols)

    return X, y, scaler
