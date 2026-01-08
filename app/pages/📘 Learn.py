import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Learn | Groundwater Intelligence",
    layout="wide"
)

# ================= SESSION STATE (LAZY LOAD) =================
if "sections_loaded" not in st.session_state:
    st.session_state.sections_loaded = 1

def load_next():
    st.session_state.sections_loaded += 1

# ================= GLOBAL CSS (UNCHANGED) =================
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #070b14;
    color: #e6f1ff;
    font-family: 'Inter', sans-serif;
}
.section { padding: 4.5rem 0; }
.section-title { font-size: 2.4rem; font-weight: 600; }
.section-text { font-size: 1.1rem; line-height: 1.8; color: #cfd8e3; }
.hero-title {
    font-size: 4rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(90deg, #6ae3ff, #4fc3f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.divider {
    width: 120px;
    height: 3px;
    background: linear-gradient(90deg, #4fc3f7, transparent);
    margin: 1.5rem 0 2.5rem 0;
}
.story-img {
    width: 72%;
    display: block;
    margin: 3rem auto;
    border-radius: 16px;
    box-shadow: 0 0 28px rgba(79,195,247,0.22);
}
.footer {
    text-align: center;
    color: #8aa0b8;
    font-size: 0.9rem;
    padding: 3rem 0 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# ================= HERO =================
st.markdown("""
<div class="section">
    <div class="hero-title">The Invisible Crisis Beneath Our Feet</div>
    <p style="text-align:center;color:#b0c4de;">
        Learning how data and intelligence understand groundwater
    </p>
</div>
""", unsafe_allow_html=True)

st.button("Scroll to continue ↓", on_click=load_next)

# ================= SECTION 1 =================
if st.session_state.sections_loaded >= 2:
    st.markdown("""
    <div class="section">
        <div class="section-title">Why Groundwater Matters</div>
        <div class="divider"></div>
        <div class="section-text">
            Groundwater provides nearly 50% of global drinking water and
            supports agriculture worldwide. Its depletion is invisible,
            slow, and often irreversible.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.image(
        "https://images.unsplash.com/photo-1509395176047-4a66953fd231",
        width=900
    )

    st.button("Continue ↓", on_click=load_next)

# ================= SECTION 2 =================
if st.session_state.sections_loaded >= 3:
    st.markdown("""
    <div class="section">
        <div class="section-title">DWLR Dataset (2023)</div>
        <div class="divider"></div>
        <div class="section-text">
            Digital Water Level Recorders continuously capture groundwater
            depth and quality across seasons and locations.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.image(
        "https://images.unsplash.com/photo-1581092580497-e0d23cbdf1dc",
        width=900
    )

    st.button("Continue ↓", on_click=load_next)

# ================= SECTION 3 – 3D (SINGLE, CLEAN) =================
if st.session_state.sections_loaded >= 4:
    st.markdown("""
    <div class="section">
        <div class="section-title">3D Relationship Understanding</div>
        <div class="divider"></div>
        <div class="section-text">
            Adjust the angle to explore how rainfall and temperature
            influence groundwater depth.
        </div>
    </div>
    """, unsafe_allow_html=True)

    angle = st.slider("Rotate view", 0, 360, 45)

    rain = np.random.uniform(0, 100, 80)
    temp = np.random.uniform(15, 40, 80)
    depth = 65 - 0.35 * rain + 0.4 * temp + np.random.normal(0, 4, 80)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(rain, temp, depth)
    ax.view_init(elev=22, azim=angle)
    ax.set_xlabel("Rainfall")
    ax.set_ylabel("Temperature")
    ax.set_zlabel("Depth")
    st.pyplot(fig)

    st.button("Continue ↓", on_click=load_next)

# ================= SECTION 4 – YOUTUBE =================
if st.session_state.sections_loaded >= 5:
    st.markdown("""
    <div class="section">
        <div class="section-title">Recommended Learning</div>
        <div class="divider"></div>
    </div>
    """, unsafe_allow_html=True)

    st.video("https://www.youtube.com/watch?v=YQ0r0JXkKzA")
    st.video("https://www.youtube.com/watch?v=IHp8k7w2u4A")
    st.video("https://www.youtube.com/watch?v=8jLOx1hD3_o")

    st.button("Continue ↓", on_click=load_next)

# ================= AI CHATBOT =================
if st.session_state.sections_loaded >= 6:
    st.markdown("""
    <div class="section">
        <div class="section-title">Ask the Model</div>
        <div class="divider"></div>
    </div>
    """, unsafe_allow_html=True)

    q = st.chat_input("Ask about the dataset, model, or visuals")
    if q:
        st.chat_message("assistant").write(
            "This project explains groundwater behavior using DWLR data and "
            "machine learning to identify patterns, not memorization."
        )

# ================= PDF EXPORT =================
if st.session_state.sections_loaded >= 6:
    if st.button("📄 Download Learn Page as PDF"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
            doc = SimpleDocTemplate(f.name)
            styles = getSampleStyleSheet()
            content = [
                Paragraph("Groundwater Intelligence – Learn Page", styles["Title"]),
                Paragraph("This document explains groundwater prediction using data and AI.", styles["BodyText"]),
            ]
            doc.build(content)
            st.download_button("Download PDF", open(f.name, "rb"), file_name="Learn_Groundwater_AI.pdf")

# ================= FOOTER =================
st.markdown("""
<div class="footer">
    © 2026 • Groundwater Intelligence System<br>
    Built for learning, research, and decision support
</div>
""", unsafe_allow_html=True)
