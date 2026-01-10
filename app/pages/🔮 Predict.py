import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
import os
from utils.floating_assistant import render_floating_assistant
if not st.session_state.get("is_authenticated"):
    st.warning("Please log in first.")
    st.page_link("app.py", label="🔐 Go to Login")
    st.stop()

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Groundwater Prediction",
    layout="wide",
    initial_sidebar_state="expanded"
)
with st.sidebar:
    st.markdown("---")
    st.markdown(
        f"""
        <div style="
            padding:12px;
            border-radius:14px;
            background:#0b1220;
            box-shadow:0 0 18px rgba(79,195,247,0.35);
            text-align:center;
        ">
            <strong>{st.session_state.user['name']}</strong><br>
            <span style="opacity:0.7">{st.session_state.user['role']}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.switch_page("app.py")

# -------------------------------------------------
# PATHS (MODEL OUTSIDE app/)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "model", "groundwater_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "model", "scaler.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# -------------------------------------------------
# SHARED THEME STATE (WITH DASHBOARD)
# -------------------------------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if st.session_state.theme == "dark":
    BG = "#020617"
    CARD = "#0b1220"
    TEXT = "#E5E7EB"
    ACCENT = "#4FC3F7"
    SIDEBAR_BG = "#050913"
else:
    BG = "#F8FAFC"
    CARD = "#FFFFFF"
    TEXT = "#0F172A"
    ACCENT = "#2563EB"
    SIDEBAR_BG = "#F1F5F9"

# -------------------------------------------------
# GLOBAL / CINEMATIC STYLES  (UNCHANGED + SIDEBAR ADDED)
# -------------------------------------------------
st.markdown(f"""
<style>
.stApp {{
    background-color: {BG};
    color: {TEXT};
}}

/* ================= DASHBOARD SIDEBAR (MATCHED) ================= */
section[data-testid="stSidebar"] {{
    width: 220px;
    background: {SIDEBAR_BG};
    transition: all 0.35s ease;
    border-right: 1px solid rgba(255,255,255,0.08);
}}

section[data-testid="stSidebar"]:hover {{
    width: 240px;
}}

section[data-testid="stSidebar"] a {{
    border-radius: 10px;
    margin: 6px 8px;
    padding: 12px 16px;
    font-size: 15px;
    transition: all 0.3s ease;
}}

section[data-testid="stSidebar"] a:hover {{
    background: rgba(79,195,247,0.18);
    transform: translateX(6px) scale(1.02);
}}

section[data-testid="stSidebar"] * {{
    color: {TEXT};
}}

/* ================= EXISTING STYLES ================= */
.card {{
    background: {CARD};
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 15px 45px rgba(0,0,0,0.4);
    transition: all 0.35s ease;
    position: relative;
    overflow: hidden;
}}

.card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 30px 80px rgba(79,195,247,0.25);
}}

.card::before {{
    content: "";
    position: absolute;
    inset: -2px;
    background: linear-gradient(
        120deg,
        transparent,
        rgba(79,195,247,0.35),
        transparent
    );
    opacity: 0;
    transition: opacity 0.4s ease;
}}

.card:hover::before {{
    opacity: 1;
}}

.prediction-value {{
    animation: pulse 2.2s infinite;
}}

@keyframes pulse {{
    0% {{ transform: scale(1); opacity: 0.9; }}
    50% {{ transform: scale(1.05); opacity: 1; }}
    100% {{ transform: scale(1); opacity: 0.9; }}
}}

[data-baseweb="slider"]:hover {{
    filter: drop-shadow(0 0 10px rgba(79,195,247,0.45));
}}

.footer {{
    margin-top: 120px;
    padding: 24px;
    text-align: center;
    opacity: 0.75;
    font-size: 14px;
}}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# TOP RIGHT ICONS
# -------------------------------------------------
spacer, user_col, theme_col = st.columns([8, 0.6, 0.6])

with user_col:
    with st.popover("👤"):
        st.page_link("pages/📊 Dashboard.py", label="📊 Dashboard")
        st.page_link("pages/🔮 Predict.py", label="🔮 Predict")
        st.page_link("pages/📘 Learn.py", label="📘 Learn")
        st.page_link("pages/🤖 Assistant.py", label="🤖 Assistant")
        st.page_link("pages/👤 Profile.py", label="👤 Profile")
        st.markdown("---")
        st.button("🚪 Logout")

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown("""
<h1 style="font-size:42px;font-weight:900;">
🔮 Groundwater Level Prediction
</h1>
<p style="max-width:760px;">
Predict <strong>shallow groundwater depth</strong> (meters below ground surface)
using environmental and water-quality indicators derived from
<strong>DWLR India – 2023</strong>.
</p>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------
# INPUT + VISUAL LAYOUT
# -------------------------------------------------
left, right = st.columns([1.1, 2])

with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🎛️ Input Parameters")

    region = st.selectbox("🌍 Region", ["India", "Other regions (Coming Soon)"])
    if region != "India":
        st.warning("This model is currently trained only on Indian groundwater data.")

    month = st.selectbox(
        "📅 Month (2023)",
        ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    )
    month_num = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"].index(month) + 1

    temp = st.slider("🌡 Temperature (°C)", 5.0, 45.0, 25.0)
    rain = st.slider("🌧 Rainfall (mm)", 0.0, 300.0, 120.0)
    ph = st.slider("🧪 pH Level", 6.0, 8.5, 7.2)
    do = st.slider("💧 Dissolved Oxygen (mg/L)", 0.5, 10.0, 4.5)

    show_aquifer = st.checkbox("Show aquifer layers")
    st.caption(
        "Aquifer layers visualize multiple underground water-bearing zones "
        "that store groundwater at different depths."
    )

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# PREDICTION LOGIC
# -------------------------------------------------
input_df = pd.DataFrame([{
    "Temperature_C": temp,
    "Rainfall_mm": rain,
    "pH": ph,
    "Dissolved_Oxygen_mg_L": do,
    "Month": month_num
}])

X_scaled = scaler.transform(input_df)
prediction = float(model.predict(X_scaled)[0])

# -------------------------------------------------
# SAVE PREDICTION (SESSION + CSV)
# -------------------------------------------------
if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

record = {
    "Month": month,
    "Prediction_m": round(prediction, 2)
}

st.session_state.prediction_history.append(record)

DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
CSV_PATH = os.path.join(DATA_DIR, "prediction_history.csv")

df_new = pd.DataFrame([record])
if os.path.exists(CSV_PATH):
    df_new.to_csv(CSV_PATH, mode="a", header=False, index=False)
else:
    df_new.to_csv(CSV_PATH, index=False)

# -------------------------------------------------
# STATUS CLASSIFICATION
# -------------------------------------------------
if prediction < 3:
    status = "Safe"
    color = "#22C55E"
elif prediction < 4.2:
    status = "Moderate"
    color = "#F59E0B"
else:
    status = "Critical"
    color = "#EF4444"

# -------------------------------------------------
# 3D GROUNDWATER + AQUIFER VISUAL
# -------------------------------------------------
with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)

    wave_strength = (prediction - 2.5) * 0.35
    Z = prediction + wave_strength * np.sin(X) * np.cos(Y)

    surfaces = [
        go.Surface(
            x=X, y=Y, z=Z,
            colorscale="Blues",
            opacity=0.95,
            showscale=False
        )
    ]

    if show_aquifer:
        for depth in [prediction + 0.5, prediction + 1.0]:
            surfaces.append(
                go.Surface(
                    x=X, y=Y,
                    z=depth + 0.1*np.sin(X)*np.cos(Y),
                    opacity=0.35,
                    showscale=False
                )
            )

    fig = go.Figure(data=surfaces)
    fig.update_layout(
        scene=dict(
            xaxis_visible=False,
            yaxis_visible=False,
            zaxis_title="Groundwater Depth (m)"
        ),
        height=460,
        transition=dict(duration=600, easing="cubic-in-out"),
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        f"""
        <h3 class="prediction-value">
        Predicted Level:
        <span style="color:{color}">{prediction:.2f} m</span>
        </h3>
        <p>Status: <strong>{status}</strong></p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# EXPLANATION + VALIDITY + FUTURE SCOPE
# -------------------------------------------------
st.markdown("""
<div class="card" style="margin-top:28px;line-height:1.7;">
<h4>🧠 What does this prediction mean?</h4>
<p>
The predicted value indicates the <strong>depth of groundwater below ground surface</strong>.
Smaller values mean water is closer and easier to access, while larger values
indicate deeper and more stressed groundwater conditions.
</p>

<h4>📊 Dataset & learning</h4>
<ul>
<li>Trained on DWLR (Digital Water Level Recorder) data from India</li>
<li>Focuses on shallow aquifers monitored across 2023</li>
<li>Learns relationships between rainfall, temperature, water quality and seasonality</li>
</ul>

<h4>⚠️ Model validity & restrictions</h4>
<ul>
<li>Best suited for groundwater depths ~2–5 meters</li>
<li>Not valid for deep confined aquifers or coastal saline zones</li>
<li>Predictions outside this range may be unreliable</li>
</ul>

<h4>🚀 Future scope</h4>
<ul>
<li>Multi-region and state-wise groundwater models</li>
<li>Seasonal and long-term forecasting</li>
<li>Groundwater depletion alerts & policy dashboards</li>
<li>Integration with satellite imagery and rainfall APIs</li>
</ul>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("""
<div class="footer">
📧 contact@groundwater.ai | ☎️ +91-XXXXXXXXXX  
<br>
© 2026 Groundwater Intelligence Platform · Feedback welcome
</div>
""", unsafe_allow_html=True)
render_floating_assistant("predict")
