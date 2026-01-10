import streamlit as st
import time

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI Assistant | Groundwater Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# THEME (MATCH APP)
# -------------------------------------------------
BG = "#020617"
CARD = "#0b1220"
TEXT = "#E5E7EB"
ACCENT = "#4FC3F7"
SIDEBAR_BG = "#050913"

# -------------------------------------------------
# GLOBAL STYLES
# -------------------------------------------------
st.markdown(f"""
<style>
.stApp {{
    background-color: {BG};
    color: {TEXT};
}}

/* ================= SIDEBAR ================= */
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

/* ================= ROBOT HERO ================= */
.robot-wrap {{
    text-align: center;
    margin: 30px 0 10px 0;
}}
.robot {{
    width: 160px;
    margin: auto;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(79,195,247,0.35), transparent 65%);
    box-shadow: 0 0 60px rgba(79,195,247,0.45);
    animation: floatBot 4.5s ease-in-out infinite;
}}
@keyframes floatBot {{
    0% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-14px); }}
    100% {{ transform: translateY(0); }}
}}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HERO
# -------------------------------------------------
st.markdown("""
<div class="robot-wrap">
  <div class="robot">
    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" width="160">
  </div>
  <h1 style="font-size:40px;font-weight:900;margin-top:16px;">
    Groundwater AI Assistant
  </h1>
  <p style="max-width:720px;margin:auto;">
    An NLP-powered assistant explaining groundwater data,
    machine learning predictions, and decision insights.
  </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------------------------
# NLP INTENT ENGINE
# -------------------------------------------------
def detect_intent(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["dataset", "dwlr", "data"]):
        return "dataset"
    if any(k in t for k in ["model", "ml", "algorithm"]):
        return "model"
    if any(k in t for k in ["prediction", "depth", "result"]):
        return "prediction"
    if any(k in t for k in ["limit", "assumption", "reliable"]):
        return "limits"
    if any(k in t for k in ["future", "scope", "next"]):
        return "future"
    return "general"

def generate_reply(intent: str) -> str:
    responses = {
        "dataset": (
            "The model is trained on DWLR (Digital Water Level Recorder) data from India (2023). "
            "It captures rainfall, temperature, pH, dissolved oxygen, seasonality, "
            "and groundwater depth."
        ),
        "model": (
            "This system uses supervised machine learning regression. "
            "It learns patterns between environmental variables rather than memorizing past values."
        ),
        "prediction": (
            "Predictions represent groundwater depth below ground surface (meters). "
            "Lower values indicate safer availability; higher values indicate stressed conditions."
        ),
        "limits": (
            "The model is best suited for shallow aquifers (~2–5 m). "
            "It is designed for decision support, not as a real-time sensor replacement."
        ),
        "future": (
            "Future scope includes multi-region models, deeper aquifer layers, "
            "seasonal forecasting, and satellite + IoT integration."
        ),
        "general": (
            "I can explain the dataset, model logic, prediction meaning, "
            "limitations, or future scope of this groundwater intelligence system."
        )
    }
    return responses[intent]

# -------------------------------------------------
# CHAT HISTORY (REAL CHAT UI)
# -------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------------------------
# CHAT INPUT (PINNED BOTTOM)
# -------------------------------------------------
user_prompt = st.chat_input("Ask me about the groundwater project…")

if user_prompt:
    # User message
    st.session_state.messages.append(
        {"role": "user", "content": user_prompt}
    )
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Assistant reply
    intent = detect_intent(user_prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            time.sleep(0.4)
            reply = generate_reply(intent)
            st.markdown(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("""
<div style="margin-top:80px;text-align:center;opacity:0.7;font-size:14px;">
This assistant demonstrates <strong>NLP intent detection</strong> and
<strong>human–AI interaction</strong> for groundwater decision support.<br>
© 2026 Groundwater Intelligence Platform
</div>
""", unsafe_allow_html=True)
