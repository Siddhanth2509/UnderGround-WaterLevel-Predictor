# 🌍 Groundwater Intelligence Platform  
### AI-Driven Groundwater Prediction & Decision Support System

🚀 **Live Streamlit App**  
👉 https://underground-intelligence.streamlit.app/ 

---

## 📌 Overview
**Groundwater Intelligence Platform** is a full-stack **Machine Learning web application** designed to **predict, visualize, and explain shallow groundwater levels** using environmental and water-quality indicators.

This project goes beyond a notebook-based ML solution and delivers a **production-ready AI product** with:
- Secure authentication
- Role-based access control
- Interactive dashboards
- 3D groundwater visualization
- NLP-powered assistant
- Cloud deployment

It aims to provide **early warning signals of groundwater stress**, enabling proactive water-resource planning.

---

## 🎯 Problem Statement
Groundwater depletion:
- Happens **gradually**
- Remains **invisible**
- Is often detected **too late**

Reactive solutions are costly and inefficient.  
This platform offers a **data-driven early-indicator system** by learning patterns between environmental factors and groundwater depth.

---

## 🧠 System Architecture

flowchart TD
    A[Environmental & Water Data] --> B[Preprocessing & Feature Engineering]
    B --> C[ML Regression Model]
    C --> D[Saved Inference Pipeline]
    D --> E[Streamlit Web Application]
    E --> F[Predictions & 3D Visualizations]
    E --> G[Admin & User Management]

⚙️ Core Features
🔐 Authentication & Roles

Login & Signup system

Admin master access

Demo mode for recruiters

Role-based UI personalization

📊 Dashboard

Groundwater prediction trends

Confidence band visualization

KPI summary cards

Interactive charts

3D groundwater & aquifer surfaces

🔮 Prediction Module

Real-time groundwater depth prediction

Uses:

🌡 Temperature

🌧 Rainfall

🧪 pH

💧 Dissolved Oxygen

📅 Seasonal indicators

Risk classification:

🟢 Safe

🟡 Moderate

🔴 Critical

📘 Learn Page (Cinematic)

Story-driven explanation of groundwater crisis

Scroll-based narrative

Visual learning aids and charts

🤖 Assistant (NLP-Focused)

Interactive chatbot

Persistent chat history

Demonstrates NLP integration in ML systems

👤 User Profile

Persistent user data

Editable personal details

Usage tracking (sessions & predictions)

🛠 Admin Panel

View registered users

Add / remove users

Password reset on request

Monitor user activity

Secure admin-only controls

📈 Model Training & Evaluation
Models Evaluated
Model	RMSE	MAE	R²
Linear Regression	0.153	0.143	-0.126
Random Forest	0.315	0.280	-3.774

✅ Linear Regression was selected due to better generalization on limited and noisy environmental data.

📊 ML Workflow
flowchart LR
    A[Raw Dataset] --> B[Cleaning & Imputation]
    B --> C[Feature Engineering]
    C --> D[Scaling]
    D --> E[Model Training]
    E --> F[Evaluation]
    F --> G[Deployment]

🎛 Expected Inputs

The prediction engine works with real-world measurable parameters:

Month (seasonality)

Temperature (°C)

Rainfall (mm)

pH level

Dissolved Oxygen (mg/L)

📁 Project Structure
UnderGround-WaterLevel-Predictor/
│
├── app/
│   ├── app.py                # Authentication & entry point
│   ├── pages/
│   │   ├── 📊 Dashboard.py
│   │   ├── 🔮 Predict.py
│   │   ├── 📘 Learn.py
│   │   ├── 🤖 Assistant.py
│   │   └── 👤 Profile.py
│   └── utils/
│       └── floating_assistant.py
│
├── src/
│   ├── preprocessing.py
│   ├── train_model.py
│   └── predict.py
│
├── data/
│   └── DWLR_Dataset_2023.csv
│
├── model/
│   ├── groundwater_model.pkl
│   ├── scaler.pkl
│   └── imputer.pkl
│
├── requirements.txt
├── .gitignore
└── README.md

▶️ Run Locally

1️⃣ Install dependencies
pip install -r requirements.txt


2️⃣ (Optional) Train the model
python src/train_model.py


3️⃣ Run the application
streamlit run app/app.py

⚠️ Limitations

Predictions are data-distribution dependent

Best suited for shallow aquifers (≈2–5 m)

Not intended for deep confined aquifers

Retraining required for new regions or long-term forecasts

🔮 Future Enhancements

🌍 Multi-region groundwater models

📈 Long-term forecasting

🛰 Satellite & rainfall API integration

🚨 Automated alert system

📱 Mobile-optimized UI

🧠 Advanced NLP reasoning in Assistant

📚 What This Project Demonstrates

End-to-end ML pipeline design

Secure authentication systems

Role-based UI architecture

Production-grade Streamlit deployment

Real-world ML trade-off decisions

AI product-level UI/UX engineering

👤 Author

Siddhanth Sharma
Machine Learning & AI Enthusiast