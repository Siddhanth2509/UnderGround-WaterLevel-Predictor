import pandas as pd
import joblib
import os

from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# ===============================
# Paths
# ===============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCALER_PATH = os.path.join(BASE_DIR, "model", "scaler.pkl")
IMPUTER_PATH = os.path.join(BASE_DIR, "model", "imputer.pkl")

# ===============================
# Columns
# ===============================
TARGET_COL = "Water_Level_m"

FEATURE_COLUMNS = [
    "Temperature_C",
    "Rainfall_mm",
    "pH",
    "Dissolved_Oxygen_mg_L",
    "DayOfYear"
]

# ===============================
# Core preprocessing
# ===============================
def load_and_preprocess_data(data, training=True):
    """
    data: CSV path or DataFrame
    training: True -> fit scaler & imputer
              False -> load saved ones
    """

    # Load data
    if isinstance(data, str):
        df = pd.read_csv(data)
    else:
        df = data.copy()

    # ---- Date handling ----
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["DayOfYear"] = df["Date"].dt.dayofyear

    # ---- Features ----
    X = df[FEATURE_COLUMNS]

    if training:
        y = df[TARGET_COL]

        # ---- Handle missing values ----
        imputer = SimpleImputer(strategy="median")
        X_imputed = imputer.fit_transform(X)

        # ---- Scaling ----
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_imputed)

        # Save artifacts
        os.makedirs(os.path.dirname(SCALER_PATH), exist_ok=True)
        joblib.dump(scaler, SCALER_PATH)
        joblib.dump(imputer, IMPUTER_PATH)

        return X_scaled, y, scaler

    else:
        imputer = joblib.load(IMPUTER_PATH)
        scaler = joblib.load(SCALER_PATH)

        X_imputed = imputer.transform(X)
        X_scaled = scaler.transform(X_imputed)

        return X_scaled, None, scaler
