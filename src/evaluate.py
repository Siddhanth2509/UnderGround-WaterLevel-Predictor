import os
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

from src.preprocessing import load_and_preprocess_data

# ===============================
# Paths
# ===============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "Data", "DWLR_Dataset_2023.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model", "groundwater_model.pkl")

def main():
    # Load data WITH y
    X, y, _ = load_and_preprocess_data(DATA_PATH, training=True)

    # Load trained model
    model = joblib.load(MODEL_PATH)

    # Predict
    y_pred = model.predict(X)

    # Metrics
    rmse = mean_squared_error(y, y_pred, squared=False)
    r2 = r2_score(y, y_pred)

    print(f"RMSE: {rmse:.3f}")
    print(f"R²  : {r2:.3f}")

    # ===============================
    # Actual vs Predicted
    # ===============================
    plt.figure(figsize=(6, 6))
    plt.scatter(y, y_pred, alpha=0.5)
    plt.plot([y.min(), y.max()], [y.min(), y.max()], "r--")
    plt.xlabel("Actual Groundwater Level (m)")
    plt.ylabel("Predicted Groundwater Level (m)")
    plt.title("Actual vs Predicted Groundwater Level")
    plt.grid(True)
    plt.show()

    # ===============================
    # Residuals
    # ===============================
    residuals = y - y_pred

    plt.figure(figsize=(6, 4))
    plt.hist(residuals, bins=30)
    plt.xlabel("Prediction Error (m)")
    plt.ylabel("Frequency")
    plt.title("Residual Distribution")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
