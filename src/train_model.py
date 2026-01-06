import os
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

from src.preprocessing import load_and_preprocess_data

# ===============================
# Paths
# ===============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "Data", "DWLR_Dataset_2023.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model", "groundwater_model.pkl")

def main():
    print("📥 Loading and preprocessing data...")
    X, y, _ = load_and_preprocess_data(DATA_PATH, training=True)

    print("🧠 Training Linear Regression model...")
    model = LinearRegression()
    model.fit(X, y)

    # Save model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    # ---- Evaluation ----
    y_pred = model.predict(X)
    rmse = mean_squared_error(y, y_pred, squared=False)
    r2 = r2_score(y, y_pred)

    print("\n✅ Training Complete")
    print(f"RMSE : {rmse:.3f}")
    print(f"R²   : {r2:.3f}")

if __name__ == "__main__":
    main()
