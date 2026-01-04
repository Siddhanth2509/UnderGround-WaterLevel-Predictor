# src/train_model.py

import os
import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from preprocessing import load_and_preprocess_data


def time_based_split(X, y, train_ratio=0.8):
    split = int(len(X) * train_ratio)
    return X.iloc[:split], X.iloc[split:], y.iloc[:split], y.iloc[split:]


def evaluate(model, X_test, y_test):
    preds = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    return rmse, mae, r2


def main():
    DATA_PATH = "Data/DWLR_Dataset_2023.csv"

    # Load data with scaling
    X, y, scaler = load_and_preprocess_data(
        DATA_PATH,
        scale_for_linear=True,
        training=True
    )

    X_train, X_test, y_train, y_test = time_based_split(X, y)

    model = LinearRegression()
    model.fit(X_train, y_train)

    rmse, mae, r2 = evaluate(model, X_test, y_test)

    print("\nLinear Regression")
    print("------------------------------")
    print(f"RMSE: {rmse:.3f}")
    print(f"MAE : {mae:.3f}")
    print(f"R²  : {r2:.3f}")

    # Ensure model folder exists
    os.makedirs("model", exist_ok=True)

    # Save model and scaler
    joblib.dump(model, "model/groundwater_model.pkl")
    joblib.dump(scaler, "model/scaler.pkl")

    print("\n✅ Linear Regression model and scaler saved")


if __name__ == "__main__":
    main()
