# src/preprocessing.py

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer


def load_and_preprocess_data(csv_path, scale_for_linear=False, training=True):


    df = pd.read_csv(csv_path)

    # Date handling
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.sort_values("Date").reset_index(drop=True)
    df = df.dropna(subset=["Date"])

    # Time features
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

    X = df[feature_cols]

    # Handle missing values
    imputer = SimpleImputer(strategy="median")
    X = pd.DataFrame(imputer.fit_transform(X), columns=feature_cols)

    scaler = None
    if scale_for_linear:
        scaler = StandardScaler()
        X = pd.DataFrame(scaler.fit_transform(X), columns=feature_cols)

    if training:
        y = df["Water_Level_m"]
        return X, y, scaler
    else:
        return X, None, scaler
