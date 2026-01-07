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
# GLOBAL STYLES
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
    transition: all 0.35s ease;
}}

.card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 30px 70px rgba(79,195,247,0.25);
}}

/* KPI */
.metric-value {{
    font-size: 28px;
    font-weight: 800;
    color: {ACCENT};
}}

.metric-label {{
    font-size: 13px;
    opacity: 0.7;
}}

/* Hero */
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

/* HIDE STREAMLIT AUTO-GENERATED MULTIPAGE NAV (app / View more) */
section[data-testid="stSidebarNav"] {{
    display: none !important;
}}

</style>



<div class="glow"></div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SIDEBAR NAVIGATION (ONLY 5 ITEMS)
# -------------------------------------------------
#with st.sidebar:
#    st.markdown("### 🌍 Navigation")
 #   st.page_link("pages/📊 Dashboard.py", label="📊 Dashboard")
#    st.page_link("pages/🔮 Predict.py", label="🔮 Predict")
#    st.page_link("pages/📘 Learn.py", label="📘 Learn")
#    st.page_link("pages/🤖 Assistant.py", label="🤖 Assistant")
#    st.page_link("pages/👤 Profile.py", label="👤 Profile")

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
# HERO SECTION (UNCHANGED)
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
# KPI CARDS (UNCHANGED)
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
# 2D TREND (UNCHANGED)
# -------------------------------------------------
st.markdown("### 📈 Prediction Trend")

data = pd.DataFrame({
    "Date": pd.date_range("2024-01-01", periods=10),
    "Water Level (m)": [3.1, 3.3, 3.4, 3.2, 3.5, 3.6, 3.4, 3.5, 3.6, 3.54]
})

fig = px.line(data, x="Date", y="Water Level (m)", markers=True)
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
# 3D VISUALS (SIDE BY SIDE)
# -------------------------------------------------
st.markdown("### 🌊 3D Groundwater & Aquifer Analysis")

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
# 3D EXPLANATION (CINEMATIC)
# -------------------------------------------------
st.markdown("""
<div style="
    margin-top: 26px;
    padding: 22px 26px;
    border-radius: 18px;
    background: rgba(79,195,247,0.08);
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
