# src/train_model.py

import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from preprocessing import load_and_preprocess_data


def time_based_split(X, y, train_ratio=0.8):
    split = int(len(X) * train_ratio)
    return X.iloc[:split], X.iloc[split:], y.iloc[:split], y.iloc[split:]


def evaluate(name, model, X_test, y_test):
    preds = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    print(f"\n{name}")
    print("-" * 30)
    print(f"RMSE: {rmse:.3f}")
    print(f"MAE : {mae:.3f}")
    print(f"R²  : {r2:.3f}")

    return rmse


def main():
    DATA_PATH = "Data/DWLR_Dataset_2023.csv"

    # Baseline
    X_lin, y_lin, _ = load_and_preprocess_data(DATA_PATH, scale_for_linear=True)
    X_tr, X_te, y_tr, y_te = time_based_split(X_lin, y_lin)

    lin = LinearRegression()
    lin.fit(X_tr, y_tr)
    rmse_lin = evaluate("Linear Regression", lin, X_te, y_te)

    # Final model
    X_rf, y_rf, _ = load_and_preprocess_data(DATA_PATH)
    X_tr, X_te, y_tr, y_te = time_based_split(X_rf, y_rf)

    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_tr, y_tr)
    rmse_rf = evaluate("Random Forest", rf, X_te, y_te)

    if rmse_rf < rmse_lin:
        joblib.dump(rf, "model/groundwater_model.pkl")
        print("\n✅ Random Forest saved")
    else:
        joblib.dump(lin, "model/groundwater_model.pkl")
        print("\n✅ Linear Regression saved")


if __name__ == "__main__":
    main()
