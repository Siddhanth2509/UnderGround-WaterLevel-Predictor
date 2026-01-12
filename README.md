# Underground Water Level Predictor

## 📌 Overview
This project is a machine learning–based system designed to predict **groundwater levels** using historical environmental data. It focuses on **localized, short-term prediction and trend analysis**, supporting early awareness of groundwater stress and encouraging preventive water resource planning.

The project follows a clean, modular ML pipeline and is designed to scale with additional data sources.

---

## 🎯 Problem Statement
Groundwater depletion often occurs gradually and remains unnoticed until severe shortages arise. Large-scale solutions like water pipelines are expensive and reactive. This project aims to provide a **data-driven early indicator** by analyzing how environmental factors affect groundwater levels.

---

## 🧠 Solution Approach
The system:
- Cleans and preprocesses raw groundwater data
- Engineers time-based and environmental features
- Trains and evaluates regression models using time-aware validation
- Selects the most reliable model
- Provides predictions for new inputs through a reusable interface

---

## ⚙️ Features
- Robust preprocessing pipeline
- Time-based train–test split
- Model comparison (baseline vs advanced)
- Evaluation using RMSE, MAE, and R²
- Prediction module for real-world usage
- Streamlit-ready architecture
- Scalable design for multi-year and multi-region data

---

## 📁 Project Structure
UnderGround-WaterLevel-Predictor/
│
├── data/
│ └── DWLR_Dataset_2023.csv
│
├── src/
│ ├── preprocessing.py # Data cleaning & feature engineering
│ ├── train_model.py # Model training & evaluation
│ └── predict.py # Model inference
│
├── model/
│ └── groundwater_model.pkl # Saved trained model
│
├── app/
│ └── streamlit_app.py # Frontend (Phase 1)
│
├── README.md
├── requirements.txt
└── .gitignore

---

## 🧪 Model Training & Evaluation

Example results:

Linear Regression

RMSE: 0.153
MAE : 0.143
R² : -0.126

Random Forest

RMSE: 0.315
MAE : 0.280
R² : -3.774


A simpler model generalized better due to limited and noisy environmental data.

---
## ▶️ How to Run

### Train the model
```bash
python src/train_model.py

➡️ Linear Regression was selected as it generalized better on limited and noisy environmental data.

▶️ How to Run the Project

1️⃣ Install dependencies
pip install -r requirements.txt


2️⃣ Train the model
python src/train_model.py


This will:

Train the model

Save the trained model and scaler in the model/ directory

3️⃣ Run prediction
python src/predict.py


Example output:

Predicted Groundwater Level: 3.541 meters

🎛️ Expected User Inputs (for UI)

The prediction system is designed to work with:

Date (for seasonal features)

Temperature (°C)

Rainfall (mm)

pH value

Dissolved Oxygen (mg/L)

These inputs reflect real-world measurable environmental conditions.

⚠️ Important Notes & Limitations

Predictions are data-distribution dependent

The model is valid only for regions with similar environmental characteristics as the training dataset

This project focuses on trend estimation, not causal hydrological modeling

Retraining is required when new regions or significantly different data are introduced

🔮 Future Enhancements

Streamlit-based interactive web interface

Confidence intervals for predictions

Lag-based and rolling-window features

Region-wise or aquifer-wise model versions

Integration with additional environmental datasets

📚 Learning Outcome

This project demonstrates:

End-to-end ML pipeline design

Separation of training and inference logic

Handling real-world preprocessing issues

Reproducible and deployable ML workflows

👤 Author

Siddhanth Sharma
