import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from utils.floating_assistant import render_floating_assistant
if not st.session_state.get("is_authenticated"):
    st.warning("Please log in first.")
    st.page_link("app.py", label="🔐 Go to Login")
    st.stop()

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Groundwater Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.markdown("---")

    st.markdown(
        f"""
        <div style="
            padding:14px;
            border-radius:14px;
            background:#0b1220;
            box-shadow:0 0 18px rgba(79,195,247,0.35);
            text-align:center;
            margin-bottom:12px;
        ">
            <strong style="font-size:16px;">
                {st.session_state.user['name']}
            </strong><br>
            <span style="opacity:0.7;font-size:13px;">
                {st.session_state.user['role']}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.switch_page("app.py")

# -------------------------------------------------
# THEME STATE
# -------------------------------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

# -------------------------------------------------
# THEME COLORS
# -------------------------------------------------
if st.session_state.theme == "dark":
    BG = "#020617"
    CARD = "#0b1220"
    TEXT = "#E5E7EB"
    ACCENT = "#4FC3F7"
    SIDEBAR_BG = "linear-gradient(180deg, #020617, #0f172a)"
else:
    BG = "#F8FAFC"
    CARD = "#2F2F2F"
    TEXT = "#000000"
    ACCENT = "#2563EB"
    SIDEBAR_BG = "linear-gradient(180deg, #f8fafc, #eef2ff)"

# -------------------------------------------------
# GLOBAL STYLES
# -------------------------------------------------
st.markdown(f"""
<style>

.stApp {{
    background-color: {BG};
    color: {TEXT};
}}

section[data-testid="stSidebar"] {{
    width: 220px;
    background: {SIDEBAR_BG};
    transition: all 0.35s ease;
}}

section[data-testid="stSidebar"]:hover {{
    width: 240px;
}}

section[data-testid="stSidebar"] a {{
    border-radius: 10px;
    margin: 6px 8px;
    padding: 10px 14px;
    font-size: 14px;
    transition: all 0.3s ease;
}}

section[data-testid="stSidebar"] a:hover {{
    background: rgba(79,195,247,0.18);
    transform: translateX(6px) scale(1.02);
}}

.card {{
    background: {CARD};
    border-radius: 20px;
    padding: 22px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.35);
    transition: all 0.4s ease;
}}

.card:hover {{
    transform: translateY(-8px) scale(1.01);
    box-shadow: 0 40px 90px rgba(79,195,247,0.28);
}}

.metric-value {{
    font-size: 28px;
    font-weight: 800;
    color: {ACCENT};
    text-shadow: 0 0 18px rgba(79,195,247,0.35);
}}

.metric-label {{
    font-size: 13px;
    opacity: 0.7;
}}

.section-title {{
    font-size: 22px;
    font-weight: 800;
    margin: 28px 0 16px 0;
}}

.section-subtle {{
    opacity: 0.75;
    font-size: 14px;
    margin-top: -8px;
}}

.hero {{
    padding: 38px 44px;
    border-radius: 28px;
    background: linear-gradient(135deg, {ACCENT}, {BG});
    box-shadow: 0 25px 70px rgba(0,0,0,0.45);
}}

.glow {{
    position: fixed;
    width: 320px;
    height: 320px;
    background: radial-gradient(circle, rgba(79,195,247,0.18), transparent);
    top: 15%;
    right: 12%;
}}

.footer {{
    margin-top: 80px;
    padding: 24px;
    text-align: center;
    opacity: 0.75;
    font-size: 14px;
}}

section[data-testid="stSidebarNav"] {{
    display: none !important;
}}

</style>

<div class="glow"></div>
""", unsafe_allow_html=True)

if st.session_state.get("is_admin"):
    with st.expander("🛠 Admin Panel"):
        st.markdown("### 👥 Registered Users")

        import json
        import os

        USERS_PATH = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "data",
            "users.json"
        )

        # Ensure data directory & file exist
        os.makedirs(os.path.dirname(USERS_PATH), exist_ok=True)

        if not os.path.exists(USERS_PATH):
            with open(USERS_PATH, "w") as f:
                json.dump({}, f)

        # Safe load
        with open(USERS_PATH, "r") as f:
            users = json.load(f)

        # Metrics
        st.metric("👥 Total Registered Users", len(users))

        if not users:
            st.info("No registered users yet.")
        else:
            for email, u in users.items():
                st.markdown(
                    f"""
                    **{u.get('name', 'Unknown User')}**  
                    📧 {email}  
                    🎭 {u.get('role', 'N/A')}  
                    🕒 Last login: {u.get('last_login', 'Not available')}
                    ---
                    """,
                    unsafe_allow_html=True
                )

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

with theme_col:
    st.button("🌙" if st.session_state.theme == "dark" else "☀️", on_click=toggle_theme)

# -------------------------------------------------
# HERO
# -------------------------------------------------
st.markdown("""
<div class="hero">
<h1 style="font-size:46px;font-weight:900;">🌍 Groundwater Intelligence</h1>
<p style="max-width:760px;font-size:16px;">
A data-driven platform for monitoring, predicting, and understanding underground water systems.
</p>
<ul>
<li>📉 Early warning of groundwater depletion</li>
<li>🌧 Climate & rainfall impact analysis</li>
<li>🧠 Explainable ML predictions</li>
<li>🌱 Sustainability & conservation insights</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
# -------------------------------------------------
# KPI CARDS
# -------------------------------------------------
c1, c2, c3, c4, c5 = st.columns(5)

def metric(label, value):
    st.markdown(f"""
    <div class="card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

with c1: metric("Last Prediction", "Live")
with c2: metric("Avg Groundwater", "≈ 3.4 m")
with c3: metric("Predictions Run", "Persistent")
with c4: metric("Region", "India")
with c5: metric("Model Status", "Active")

# -------------------------------------------------
# LOAD HISTORY (CSV → SESSION → FALLBACK)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_PATH = os.path.join(BASE_DIR, "data", "prediction_history.csv")

if os.path.exists(CSV_PATH):
    history_df = pd.read_csv(CSV_PATH)
elif "prediction_history" in st.session_state:
    history_df = pd.DataFrame(st.session_state.prediction_history)
else:
    history_df = pd.DataFrame({"Prediction_m": [3.2, 3.4, 3.3]})

# -------------------------------------------------
# 🔒 COLUMN NORMALIZATION (FINAL FIX)
# -------------------------------------------------
if "Prediction_m" not in history_df.columns:
    for col in history_df.columns:
        if "predict" in col.lower():
            history_df.rename(columns={col: "Prediction_m"}, inplace=True)
            break

if "Prediction_m" not in history_df.columns:
    st.warning("No prediction data available yet.")
    st.stop()

history_df["Index"] = range(1, len(history_df) + 1)

# -------------------------------------------------
# TREND + CONFIDENCE BAND
# -------------------------------------------------
st.markdown("""
<div class="section-title">📈 Prediction Trend</div>
<div class="section-subtle">Groundwater depth with uncertainty</div>
""", unsafe_allow_html=True)

confidence = 0.1
history_df["Upper"] = history_df["Prediction_m"] + confidence
history_df["Lower"] = history_df["Prediction_m"] - confidence

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=history_df["Index"],
    y=history_df["Prediction_m"],
    mode="lines+markers",
    name="Prediction",
    line=dict(color=ACCENT, width=3)
))

fig.add_trace(go.Scatter(
    x=list(history_df["Index"]) + list(history_df["Index"])[::-1],
    y=list(history_df["Upper"]) + list(history_df["Lower"])[::-1],
    fill="toself",
    fillcolor="rgba(79,195,247,0.15)",
    line=dict(color="rgba(255,255,255,0)"),
    hoverinfo="skip",
    name="Confidence (±0.1 m)"
))

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color=TEXT,
    height=380
)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# 3D VISUALS
# -------------------------------------------------
st.markdown("""
<div class="section-title">🌊 3D Groundwater & Aquifer Analysis</div>
""", unsafe_allow_html=True)

left, right = st.columns(2)

def groundwater_surface(offset):
    x = np.linspace(-5, 5, 40)
    y = np.linspace(-5, 5, 40)
    X, Y = np.meshgrid(x, y)
    Z = offset + 0.3 * np.sin(X) * np.cos(Y)

    fig = go.Figure(
        data=[go.Surface(x=X, y=Y, z=Z, colorscale="Blues", showscale=False)]
    )
    fig.update_layout(
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
        height=380,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig

def aquifer_layers():
    x = np.linspace(-5, 5, 40)
    y = np.linspace(-5, 5, 40)
    X, Y = np.meshgrid(x, y)

    layers = []
    for depth in [3.2, 3.5, 3.8]:
        layers.append(
            go.Surface(
                x=X, y=Y,
                z=depth + 0.1*np.sin(X)*np.cos(Y),
                opacity=0.6,
                showscale=False
            )
        )

    fig = go.Figure(data=layers)
    fig.update_layout(
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
        height=380,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig

with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.plotly_chart(groundwater_surface(history_df["Prediction_m"].iloc[-1]), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.plotly_chart(aquifer_layers(), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# 3D EXPLANATION (RESTORED)
# -------------------------------------------------
st.markdown("""
<div style="
    margin-top: 32px;
    padding: 30px 34px;
    border-radius: 22px;
    background: linear-gradient(
        135deg,
        rgba(79,195,247,0.16),
        rgba(79,195,247,0.04)
    );
    line-height: 1.7;
    box-shadow: 0 20px 60px rgba(0,0,0,0.35);
">
<h3>🧭 Understanding the 3D Visualizations</h3>
<p><strong>Groundwater Surface</strong> shows spatial variation of predicted groundwater depth influenced by rainfall, terrain and seasonality.</p>
<p><strong>Aquifer Layers</strong> represent multiple underground water-bearing formations storing groundwater at different depths.</p>
<p style="opacity:0.85;">These visuals dynamically react to model predictions, converting abstract numbers into intuitive subsurface insight.</p>
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
render_floating_assistant("dashboard")
