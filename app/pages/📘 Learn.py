import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from utils.floating_assistant import render_floating_assistant
if not st.session_state.get("is_authenticated"):
    st.warning("Please log in first.")
    st.page_link("app.py", label="🔐 Go to Login")
    st.stop()
# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Learn | Groundwater Intelligence",
    layout="wide"
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

# ================= GLOBAL CSS (UNCHANGED) =================
st.markdown("""
<style>

/* ========= RESET ========= */
.stApp, .stAppViewContainer, .main {
    background: none !important;
}

/* ========= MAIN BACKGROUND ========= */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background:
        radial-gradient(1600px 800px at 18% 12%, rgba(35,115,255,0.22), transparent 45%),
        radial-gradient(1200px 700px at 82% 22%, rgba(0,180,255,0.18), transparent 50%),
        radial-gradient(1400px 900px at 50% 90%, rgba(0,95,185,0.20), transparent 55%),
        linear-gradient(180deg, #03060c 0%, #070b14 45%, #03060c 100%);
    z-index: 0;
}

/* ========= VIGNETTE ========= */
.stApp::after {
    content: "";
    position: fixed;
    inset: 0;
    box-shadow: inset 0 0 180px rgba(0,0,0,0.9);
    pointer-events: none;
    z-index: 1;
}

/* ========= CONTENT LAYER ========= */
.block-container {
    position: relative;
    z-index: 2;
    background: transparent !important;
}

/* ========= SIDEBAR (MATCH PREDICT) ========= */
section[data-testid="stSidebar"] {
    width: 220px;
    background: #050913;
    transition: all 0.35s ease;
    border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"]:hover {
    width: 240px;
}
section[data-testid="stSidebar"] a {
    border-radius: 10px;
    margin: 6px 8px;
    padding: 12px 16px;
    font-size: 15px;
    transition: all 0.3s ease;
}
section[data-testid="stSidebar"] a:hover {
    background: rgba(79,195,247,0.18);
    transform: translateX(6px) scale(1.02);
}
section[data-testid="stSidebar"] * {
    color: #E5E7EB;
}

/* ========= PROGRESS BAR ========= */
#progress-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 5px;
    background: rgba(255,255,255,0.05);
    z-index: 9999;
}
#progress-bar {
    height: 5px;
    width: 0%;
    background: linear-gradient(90deg, #4fc3f7, #6ae3ff);
}

/* ========= SECTIONS ========= */
.section {
    padding: 3.8rem 0;
    animation: fadeUp 1.15s ease both;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(22px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ========= TYPOGRAPHY ========= */
.hero-title {
    font-size: 4.2rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(90deg, #6ae3ff, #4fc3f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 35px rgba(0,160,255,0.45);
}
.section-title {
    font-size: 2.5rem;
    font-weight: 600;
}
.section-text {
    font-size: 1.15rem;
    line-height: 1.7;
    color: #cfd8e3;
    max-width: 940px;
}

/* ========= DIVIDER ========= */
.divider {
    width: 120px;
    height: 3px;
    background: linear-gradient(90deg, #4fc3f7, transparent);
    margin: 1.3rem 0 2rem 0;
}

/* ========= CARDS ========= */
.card {
    background: rgba(255,255,255,0.045);
    border-radius: 18px;
    padding: 1.9rem;
    border: 1px solid rgba(255,255,255,0.08);
    transition: transform .3s ease, box-shadow .3s ease;
}
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 0 38px rgba(79,195,247,0.45);
}

/* ========= FOOTER ========= */
.footer {
    text-align: center;
    color: #9bb0c7;
    font-size: 0.95rem;
    padding: 3rem 0 1rem 0;
}
</style>

<div id="progress-container"><div id="progress-bar"></div></div>

<script>
window.addEventListener("scroll", () => {
    const scrolled = (document.documentElement.scrollTop /
    (document.documentElement.scrollHeight - document.documentElement.clientHeight)) * 100;
    document.getElementById("progress-bar").style.width = scrolled + "%";
});
</script>
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

# ================= HERO =================
st.markdown("""
<div class="section">
  <div class="hero-title">The Invisible Crisis Beneath Our Feet</div>
  <p style="text-align:center;color:#b7cbe6;max-width:940px;margin:auto;">
    Groundwater is hidden, slow to respond, and easy to overuse.
    This page walks you through <b>why it matters</b>,
    <b>how data captures it</b>, and <b>how AI helps us reason about it</b>.
  </p>
</div>
""", unsafe_allow_html=True)

# ================= WHY GROUNDWATER MATTERS =================
st.markdown("""
<div class="section">
  <div class="section-title">Why Groundwater Matters</div>
  <div class="divider"></div>
  <div class="section-text">
    <b>The problem:</b> Groundwater depletion happens silently, underground, and often goes unnoticed
    until wells fail or ecosystems collapse.<br><br>

    <b>The impact:</b> Nearly 50% of global drinking water and most irrigation systems depend on groundwater.
    Declining levels increase pumping costs, reduce crop yields, and threaten water security.<br><br>

    <b>The urgency:</b> Unlike surface water, groundwater recovers slowly. Decisions made today
    affect availability for decades.
  </div>
</div>
""", unsafe_allow_html=True)

st.image("https://images.unsplash.com/photo-1509395176047-4a66953fd231", use_container_width=True)

# ================= DATASET STORY =================
st.markdown("""
<div class="section">
  <div class="section-title">Dataset Story — DWLR 2023</div>
  <div class="divider"></div>
  <div class="section-text">
    Digital Water Level Recorders (DWLRs) are installed across India to continuously
    monitor groundwater depth and quality indicators throughout the year.<br><br>

    This dataset captures seasonal variation, recharge cycles, and human impact,
    turning raw sensor readings into meaningful learning signals.
  </div>
</div>
""", unsafe_allow_html=True)

cols = st.columns(5)
features = [
    ("🌧 Rainfall", "Controls recharge and seasonal recovery"),
    ("🧪 pH", "Indicates chemical balance and contamination risk"),
    ("💧 DO", "Reflects groundwater quality"),
    ("🌡 Temperature", "Captures seasonal and chemical dynamics"),
    ("⬇ Depth", "Direct measure of groundwater availability"),
]
for col, (t, d) in zip(cols, features):
    with col:
        st.markdown(f"<div class='card'><h3>{t}</h3><p>{d}</p></div>", unsafe_allow_html=True)

st.image("https://images.unsplash.com/photo-1581092580497-e0d23cbdf1dc", use_container_width=True)

# ================= HOW THE MODEL THINKS =================
st.markdown("""
<div class="section">
  <div class="section-title">How the Model Thinks</div>
  <div class="divider"></div>
  <div class="section-text">
    The model does <b>not</b> memorize past groundwater levels.<br><br>

    Instead, it learns relationships:
    how rainfall interacts with temperature,
    how water quality reflects subsurface conditions,
    and how seasonal patterns influence depth.<br><br>

    This distinction — <b>pattern learning vs memorization</b> —
    allows the model to generalize to unseen conditions.
  </div>
</div>
""", unsafe_allow_html=True)

st.image("https://images.unsplash.com/photo-1555949963-aa79dcee981c", use_container_width=True)

# ================= 3D UNDERSTANDING =================
st.markdown("""
<div class="section">
  <div class="section-title">Understanding Relationships in 3D</div>
  <div class="divider"></div>
  <div class="section-text">
    Groundwater depth is influenced by multiple variables simultaneously.
    A 3D view helps reveal how these variables interact together,
    rather than in isolation.
  </div>
</div>
""", unsafe_allow_html=True)

angle = st.slider("Rotate 3D View", 0, 360, 45)
x = np.random.uniform(0, 100, 70)
y = np.random.uniform(15, 40, 70)
z = 65 - 0.35 * x + 0.4 * y + np.random.normal(0, 4, 70)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.scatter(x, y, z)
ax.view_init(22, angle)
st.pyplot(fig)

# ================= LIMITS & ASSUMPTIONS =================
st.markdown("""
<div class="section">
  <div class="section-title">Limits & Assumptions</div>
  <div class="divider"></div>
  <div class="section-text">
    • Predictions remain within physically observed ranges<br>
    • Designed as <b>decision support</b>, not a real-time sensor<br>
    • Accuracy depends on data coverage and representativeness<br>
    • Extreme or unobserved conditions may reduce reliability
  </div>
</div>
""", unsafe_allow_html=True)

st.image("https://images.unsplash.com/photo-1618477461853-cf6ed80faba5", use_container_width=True)

# ================= FUTURE SCOPE =================
st.markdown("""
<div class="section">
  <div class="section-title">Future Scope</div>
  <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)
future = [
    ("🌍 Multi-Region Models", "State & basin-level forecasting"),
    ("🕳 Deeper Aquifers", "Multi-layer aquifer modeling"),
    ("🛰 Satellite + IoT", "Near real-time recharge and extraction signals"),
]
for col, (t, d) in zip([f1, f2, f3], future):
    with col:
        st.markdown(f"<div class='card'><h3>{t}</h3><p>{d}</p></div>", unsafe_allow_html=True)

# ================= LEARNING =================
st.markdown("""
<div class="section">
  <div class="section-title">Recommended Learning Resources</div>
  <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

st.video("https://www.youtube.com/watch?v=zJgukuGKBUc")
st.video("https://www.youtube.com/watch?v=IJaQUOj2Tg4")
st.video("https://www.youtube.com/watch?v=b4WAxXXNSM4")

# ================= FOOTER =================
st.markdown("""
<div class="footer">
  © 2026 • Groundwater Intelligence System<br>
  Built for learning, research, and decision support
</div>
""", unsafe_allow_html=True)
render_floating_assistant("learn")
