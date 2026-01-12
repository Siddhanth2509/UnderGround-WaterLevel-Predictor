🌍 Groundwater Intelligence Platform
AI-Driven Groundwater Prediction & Decision Support System

🔗 Live App (Streamlit Cloud):
👉[ https://groundwater-intelligence.streamlit.app](https://underground-intelligence.streamlit.app/)

📌 Overview

Groundwater Intelligence Platform is a full-stack machine learning–powered web application designed to predict, visualize, and analyze shallow groundwater levels using environmental and water-quality indicators.

Unlike notebook-only ML projects, this system delivers a production-ready AI product featuring:

Secure authentication

Role-based access (User / Demo / Admin)

Interactive 3D visualizations

Cinematic UI/UX

Admin user management

Cloud deployment

It enables early detection of groundwater stress, helping researchers, planners, and policymakers make informed decisions before critical depletion occurs.

🎯 Problem Statement

Groundwater depletion is:

Gradual

Invisible

Detected too late

Large infrastructure solutions are expensive and reactive.
This project provides a data-driven early-warning system by learning relationships between environmental factors and groundwater depth.

🧠 Solution Architecture

End-to-end AI system, not just a model.

Raw Environmental Data
        ↓
Preprocessing & Feature Engineering
        ↓
ML Regression Model
        ↓
Saved Inference Pipeline
        ↓
Secure Streamlit Web App
        ↓
Visualization • Prediction • Insights

⚙️ Core Features
🔐 Authentication & Roles

Login / Signup system

Admin master access

Demo mode for recruiters

Role-based UI personalization

📊 Dashboard

Prediction trend with confidence band

KPI cards (status, region, model health)

Interactive charts

3D groundwater & aquifer surfaces

Persistent user context

🔮 Prediction Engine

Real-time groundwater depth prediction

Uses:

Temperature

Rainfall

pH

Dissolved Oxygen

Seasonal features

3D animated subsurface visualization

Status classification (Safe / Moderate / Critical)

📘 Learn (Cinematic Scroll)

Story-driven explanation of groundwater crisis

Visual learning sections

Educational charts & animations

🤖 Assistant (NLP-Focused)

Context-aware chatbot

Chat history persistence

File & dataset discussion support

Designed to demonstrate NLP integration skills

👤 Profile

Persistent user profile

Usage metrics (sessions, predictions)

Editable details

Avatar support

🛠 Admin Panel

View all registered users

Reset passwords (on request)

Add / remove users

Monitor last login & activity

Secure admin-only controls

📈 Model Training & Evaluation

The model focuses on short-term, localized groundwater depth prediction.

Models Evaluated
Model	RMSE	MAE	R²
Linear Regression	0.153	0.143	−0.126
Random Forest	0.315	0.280	−3.774

➡️ Linear Regression generalized better due to limited and noisy environmental data and was selected for deployment.

🎛️ Expected Inputs

The prediction system works with real-world measurable parameters:

Month (seasonality)

Temperature (°C)

Rainfall (mm)

pH level

Dissolved Oxygen (mg/L)

📁 Project Structure
UnderGround-WaterLevel-Predictor/
│
├── app/
│   ├── app.py                # Login / Signup / Admin / Demo
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

▶️ Running Locally
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Train model (optional)
python src/train_model.py

3️⃣ Run the app
streamlit run app/app.py

⚠️ Important Notes & Limitations

Predictions are data-distribution dependent

Best suited for shallow aquifers (~2–5m)

Not intended for deep confined aquifers or coastal saline zones

Retraining required for new regions or long-term forecasting

🔮 Future Enhancements

Multi-region groundwater models

Long-term forecasting

Satellite & rainfall API integration

Automated alert system

Mobile-optimized UI

Advanced NLP reasoning in Assistant

📚 What This Project Demonstrates

End-to-end ML pipeline design

Secure authentication & role-based systems

Production Streamlit architecture

Cloud deployment & debugging

UI/UX engineering for AI products

Real-world ML tradeoff decisions

👤 Author

Siddhanth Sharma
Machine Learning & AI Enthusiast
