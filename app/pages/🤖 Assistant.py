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
# GLOBAL STYLES (CINEMATIC + HOVER FIXED)
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
    margin: 36px 0 18px 0;
}}

.robot {{
    width: 160px;
    margin: auto;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(79,195,247,0.35), transparent 65%);
    box-shadow: 0 0 50px rgba(79,195,247,0.35);
    animation: floatBot 5s ease-in-out infinite;
    transition: transform 0.4s ease, box-shadow 0.4s ease;
}}

.robot:hover {{
    transform: scale(1.06);
    box-shadow: 0 0 80px rgba(79,195,247,0.6);
}}

@keyframes floatBot {{
    0% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-14px); }}
    100% {{ transform: translateY(0); }}
}}

/* Speaking pulse */
.speaking {{
    animation: speakPulse 1.2s ease-in-out infinite;
}}

@keyframes speakPulse {{
    0% {{ box-shadow: 0 0 40px rgba(79,195,247,0.3); }}
    50% {{ box-shadow: 0 0 90px rgba(79,195,247,0.75); }}
    100% {{ box-shadow: 0 0 40px rgba(79,195,247,0.3); }}
}}

/* ================= CHAT ================= */
.chat-card {{
    background: {CARD};
    border-radius: 22px;
    padding: 28px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.55);
}}

.msg {{
    padding: 14px 18px;
    border-radius: 16px;
    margin: 14px 0;
    animation: slideIn 0.45s ease;
}}

@keyframes slideIn {{
    from {{ opacity: 0; transform: translateY(12px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.user {{
    background: rgba(79,195,247,0.18);
}}

.bot {{
    background: rgba(255,255,255,0.07);
}}

/* ================= PROMPT CHIPS ================= */
.prompt-chip {{
    display: inline-block;
    padding: 8px 16px;
    border-radius: 20px;
    background: rgba(79,195,247,0.14);
    margin: 6px 6px 0 0;
    cursor: pointer;
    transition: all 0.25s ease;
}}

.prompt-chip:hover {{
    background: rgba(79,195,247,0.3);
    transform: translateY(-4px);
}}

.footer {{
    margin-top: 90px;
    padding: 24px;
    text-align: center;
    opacity: 0.75;
    font-size: 14px;
}}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HERO
# -------------------------------------------------
speaking = st.session_state.get("is_speaking", False)
robot_class = "robot speaking" if speaking else "robot"

st.markdown(f"""
<div class="robot-wrap">
  <div class="{robot_class}">
    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" width="160">
  </div>
  <h1 style="font-size:40px;font-weight:900;margin-top:16px;">
    Groundwater AI Assistant
  </h1>
  <p style="max-width:720px;margin:auto;">
    An intelligent NLP-based assistant explaining groundwater data,
    machine learning predictions, and decision insights.
  </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SESSION STATE (SAFE)
# -------------------------------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

st.session_state.is_speaking = False

# -------------------------------------------------
# NLP ENGINE (STABLE)
# -------------------------------------------------
def detect_intent(text):
    t = text.lower()
    if any(k in t for k in ["dataset", "dwlr", "data"]):
        return "dataset"
    if any(k in t for k in ["model", "ml", "algorithm"]):
        return "model"
    if any(k in t for k in ["prediction", "depth", "result"]):
        return "prediction"
    if any(k in t for k in ["limit", "reliable", "assumption"]):
        return "limits"
    if any(k in t for k in ["future", "scope", "next"]):
        return "future"
    return "general"

def generate_reply(intent):
    return {
        "dataset": "The system is trained on DWLR (Digital Water Level Recorder) data from India (2023), capturing rainfall, temperature, pH, dissolved oxygen, seasonality, and groundwater depth.",
        "model": "The model uses supervised machine learning to learn relationships between environmental factors and groundwater depth rather than memorizing past values.",
        "prediction": "Predictions represent groundwater depth below ground surface (meters). Lower values indicate safer availability, while higher values indicate stressed conditions.",
        "limits": "The model is designed for shallow aquifers (~2–5 m) and for decision support, not as a real-time sensor replacement.",
        "future": "Future scope includes multi-region models, deeper aquifer layers, seasonal forecasting, and satellite + IoT integration.",
        "general": "I can explain the dataset, model logic, prediction meaning, limitations, or future scope of this groundwater intelligence system."
    }[intent]

# -------------------------------------------------
# HANDLE INPUT (NO LOOPS)
# -------------------------------------------------
user_text = st.text_input("Ask me about the project…")

if user_text:
    st.session_state.pending_prompt = user_text

if st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

    st.session_state.chat.append({"role": "user", "content": prompt})

    st.session_state.is_speaking = True
    time.sleep(0.35)

    intent = detect_intent(prompt)
    reply = generate_reply(intent)

    st.session_state.chat.append({"role": "assistant", "content": reply})
    st.session_state.is_speaking = False

# -------------------------------------------------
# CHAT DISPLAY
# -------------------------------------------------
st.markdown("<div class='chat-card'>", unsafe_allow_html=True)

for msg in st.session_state.chat:
    cls = "user" if msg["role"] == "user" else "bot"
    icon = "🧑" if msg["role"] == "user" else "🤖"
    st.markdown(
        f"<div class='msg {cls}'>{icon} {msg['content']}</div>",
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# PROMPTS (NO RERUN)
# -------------------------------------------------
st.markdown("**Try asking:**")

for p in [
    "Explain the dataset",
    "How does the model work?",
    "What does a prediction mean?",
    "What are the limitations?",
    "What is the future scope?"
]:
    if st.button(p):
        st.session_state.pending_prompt = p

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("""
<div class="footer">
This assistant demonstrates <strong>NLP intent detection,
context awareness, and human–AI interaction</strong> for groundwater decision support.<br>
© 2026 Groundwater Intelligence Platform
</div>
""", unsafe_allow_html=True)
