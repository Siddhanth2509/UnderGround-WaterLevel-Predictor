import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Groundwater Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
# GLOBAL STYLES (UX POLISH ONLY)
# -------------------------------------------------
st.markdown(f"""
<style>

.stApp {{
    background-color: {BG};
    color: {TEXT};
}}

/* ---------- SIDEBAR ---------- */
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

/* ---------- CARDS ---------- */
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

/* ---------- KPI ---------- */
.metric-value {{
    font-size: 28px;
    font-weight: 800;
    color: {ACCENT};
    text-shadow: 0 0 18px rgba(79,195,247,0.35);
}}

.metric-label {{
    font-size: 13px;
    opacity: 0.7;
    letter-spacing: 0.3px;
}}

/* ---------- SECTION TITLES ---------- */
.section-title {{
    font-size: 22px;
    font-weight: 800;
    margin: 28px 0 16px 0;
    letter-spacing: 0.4px;
}}

.section-subtle {{
    opacity: 0.75;
    font-size: 14px;
    margin-top: -8px;
}}

/* ---------- HERO ---------- */
.hero {{
    padding: 38px 44px;
    border-radius: 28px;
    background: linear-gradient(135deg, {ACCENT}, {BG});
    box-shadow: 0 25px 70px rgba(0,0,0,0.45);
}}

/* Glow */
.glow {{
    position: fixed;
    width: 320px;
    height: 320px;
    background: radial-gradient(circle, rgba(79,195,247,0.18), transparent);
    top: 15%;
    right: 12%;
    z-index: 0;
}}

/* Floating chatbot */
.chatbot {{
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: {ACCENT};
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 24px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.35);
    cursor: pointer;
    transition: transform 0.3s ease;
}}

.chatbot:hover {{
    transform: scale(1.1);
}}

/* Footer */
.footer {{
    margin-top: 80px;
    padding: 24px;
    text-align: center;
    opacity: 0.75;
    font-size: 14px;
}}

/* Hide Streamlit auto nav */
section[data-testid="stSidebarNav"] {{
    display: none !important;
}}

</style>

<div class="glow"></div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# TOP RIGHT ICONS (UNCHANGED)
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
# HERO SECTION
# -------------------------------------------------
st.markdown("""
<div class="hero">
    <h1 style="font-size:46px;font-weight:900;">
        🌍 Groundwater Intelligence
    </h1>
    <p style="max-width:760px;font-size:16px;">
        A data-driven platform for monitoring, predicting, and understanding
        underground water systems using machine learning and scientific insights.
    </p>
    <ul style="margin-top:12px;">
        <li>📉 Early warning of groundwater depletion</li>
        <li>🌧️ Climate & rainfall impact analysis</li>
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

with c1: metric("Last Prediction", "3.54 m")
with c2: metric("Avg Groundwater", "3.43 m")
with c3: metric("Predictions Run", "12")
with c4: metric("Region", "India")
with c5: metric("Model Status", "Active")

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------
# 2D TREND
# -------------------------------------------------
st.markdown("""
<div class="section-title">📈 Prediction Trend</div>
<div class="section-subtle">Temporal evolution of groundwater depth</div>
""", unsafe_allow_html=True)

#data = pd.DataFrame({
#    "Date": pd.date_range("2024-01-01", periods=10),
#    "Water Level (m)": [3.1, 3.3, 3.4, 3.2, 3.5, 3.6, 3.4, 3.5, 3.6, 3.54]
#})
# -------------------------------------------------
# LIVE PREDICTION HISTORY (FROM PREDICT PAGE)
# -------------------------------------------------
if "prediction_history" in st.session_state and len(st.session_state.prediction_history) > 0:
    data = pd.DataFrame(st.session_state.prediction_history)
    data["Index"] = range(1, len(data) + 1)
    x_col = "Index"
    y_col = "Prediction_m"
else:
    # Fallback if no predictions yet
    data = pd.DataFrame({
        "Index": [1, 2, 3],
        "Prediction_m": [3.2, 3.4, 3.3]
    })
    x_col = "Index"
    y_col = "Prediction_m"


#fig = px.line(data, x="Date", y="Water Level (m)", markers=True)
fig = px.line(
    data,
    x=x_col,
    y=y_col,
    markers=True
)

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
<div class="section-subtle">Subsurface water dynamics and aquifer stratification</div>
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
    st.plotly_chart(groundwater_surface(3.5), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.plotly_chart(aquifer_layers(), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# 3D EXPLANATION
# -------------------------------------------------
st.markdown("""
<div style="
    margin-top: 26px;
    padding: 22px 26px;
    border-radius: 18px;
    background: linear-gradient(
        135deg,
        rgba(79,195,247,0.10),
        rgba(79,195,247,0.03)
    );
    line-height: 1.6;
">
    <h4>🧭 Understanding the 3D Visualizations</h4>
    <p>
        <strong>Groundwater Surface</strong> illustrates how underground water
        levels vary across a region due to rainfall, terrain, and seasonal effects.
    </p>
    <p>
        <strong>Aquifer Layers</strong> represent multiple water-bearing zones
        beneath the surface, revealing how groundwater is stored at different depths.
    </p>
    <p style="opacity:0.85;">
        These visualizations convert complex data into an intuitive picture of
        what lies beneath the earth.
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# CHATBOT ICON
# -------------------------------------------------
st.markdown("""<div class="chatbot">🤖</div>""", unsafe_allow_html=True)

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
