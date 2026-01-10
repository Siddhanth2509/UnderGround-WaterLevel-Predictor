import streamlit as st
import pandas as pd
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
# THEME
# -------------------------------------------------
BG = "#020617"
CARD = "#0b1220"
TEXT = "#E5E7EB"
ACCENT = "#4FC3F7"
SIDEBAR_BG = "#050913"

# -------------------------------------------------
# GLOBAL STYLES (HOVER + CINEMATIC)
# -------------------------------------------------
st.markdown(f"""
<style>
.stApp {{
    background:
        radial-gradient(1200px 600px at 10% 10%, rgba(79,195,247,0.15), transparent 40%),
        radial-gradient(1000px 600px at 90% 20%, rgba(99,102,241,0.18), transparent 45%),
        linear-gradient(180deg, #020617, #030b1c);
    color: {TEXT};
}}

/* ================= SIDEBAR ================= */
section[data-testid="stSidebar"] {{
    width: 220px;
    background: {SIDEBAR_BG};
    transition: all 0.35s ease;
}}
section[data-testid="stSidebar"]:hover {{
    width: 240px;
}}

section[data-testid="stSidebar"] button {{
    width: 100%;
    border-radius: 10px;
    margin: 6px 0;
    padding: 10px 14px;
    font-size: 14px;
    transition: all 0.3s ease;
}}

section[data-testid="stSidebar"] button:hover {{
    background: rgba(79,195,247,0.18);
    transform: translateX(6px) scale(1.03);
    box-shadow: 0 0 18px rgba(79,195,247,0.35);
}}

section[data-testid="stSidebar"] * {{
    color: {TEXT};
}}

/* ================= CHAT ================= */
.chat-msg {{
    padding: 18px 22px;
    border-radius: 18px;
    margin: 14px 0;
    font-size: 1.15rem;
    line-height: 1.65;
    animation: slideUp 0.4s ease;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}}

.chat-msg:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(79,195,247,0.25);
}}

@keyframes slideUp {{
    from {{ opacity: 0; transform: translateY(14px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.user {{ background: rgba(79,195,247,0.22); }}
.bot {{ background: rgba(255,255,255,0.08); }}

/* ================= ROBOT ================= */
.robot {{
    width: 160px;
    margin: auto;
    border-radius: 50%;
    box-shadow: 0 0 80px rgba(79,195,247,0.45);
    animation: float 4.5s ease-in-out infinite;
    transition: transform 0.4s ease, box-shadow 0.4s ease;
}}

.robot:hover {{
    transform: scale(1.07);
    box-shadow: 0 0 110px rgba(79,195,247,0.75);
}}

@keyframes float {{
    50% {{ transform: translateY(-14px); }}
}}

/* ================= FOOTER ================= */
.footer {{
    margin-top: 80px;
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
# SESSION STATE
# -------------------------------------------------
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {"Chat 1": []}

if "active_chat" not in st.session_state:
    st.session_state.active_chat = "Chat 1"

if "uploaded_context" not in st.session_state:
    st.session_state.uploaded_context = ""

# -------------------------------------------------
# SIDEBAR – CHAT HISTORY + DELETE
# -------------------------------------------------
st.sidebar.markdown("## 💬 Chat History")

to_delete = None

for chat_name in list(st.session_state.chat_sessions.keys()):
    col1, col2 = st.sidebar.columns([4, 1])

    with col1:
        if st.button(chat_name, key=f"open_{chat_name}"):
            st.session_state.active_chat = chat_name

    with col2:
        if st.button("🗑", key=f"del_{chat_name}"):
            to_delete = chat_name

if to_delete:
    del st.session_state.chat_sessions[to_delete]
    if not st.session_state.chat_sessions:
        st.session_state.chat_sessions = {"Chat 1": []}
        st.session_state.active_chat = "Chat 1"
    else:
        st.session_state.active_chat = list(st.session_state.chat_sessions.keys())[0]
    st.rerun()

if st.sidebar.button("➕ New Chat"):
    new_name = f"Chat {len(st.session_state.chat_sessions) + 1}"
    st.session_state.chat_sessions[new_name] = []
    st.session_state.active_chat = new_name
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("## 📎 Upload File")

uploaded = st.sidebar.file_uploader(
    "Upload CSV or TXT file",
    type=["csv", "txt"]
)

if uploaded:
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
        st.session_state.uploaded_context = df.head().to_string()
    elif uploaded.name.endswith(".txt"):
        st.session_state.uploaded_context = uploaded.read().decode("utf-8")[:2000]

# -------------------------------------------------
# HERO
# -------------------------------------------------
st.markdown("""
<div style="text-align:center;margin-top:30px;">
  <img class="robot" src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png">
  <h1 style="font-size:42px;font-weight:900;">Groundwater AI Assistant</h1>
  <p>Ask questions about the project, dataset, model, predictions, or uploaded files.</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# NLP ENGINE
# -------------------------------------------------
def detect_intent(text):
    t = text.lower()
    if "dataset" in t or "csv" in t:
        return "dataset"
    if "model" in t or "ml" in t:
        return "model"
    if "prediction" in t:
        return "prediction"
    if "file" in t or "upload" in t:
        return "file"
    return "general"

def generate_reply(prompt):
    intent = detect_intent(prompt)

    if intent == "file" and st.session_state.uploaded_context:
        return (
            "Here is a preview from the uploaded file:\n\n"
            f"{st.session_state.uploaded_context[:600]}"
        )

    if intent == "dataset":
        return (
            "This project uses DWLR 2023 groundwater data including rainfall, "
            "temperature, pH, dissolved oxygen, and groundwater depth."
        )

    if intent == "model":
        return (
            "The model is a supervised machine learning regression system that "
            "learns patterns between environmental variables and groundwater depth."
        )

    if intent == "prediction":
        return (
            "Predictions represent groundwater depth below ground surface. "
            "Higher values indicate stressed groundwater conditions."
        )

    return (
        "I can help explain the dataset, model logic, predictions, limitations, "
        "or answer questions based on uploaded CSV or TXT files."
    )

# -------------------------------------------------
# CHAT DISPLAY
# -------------------------------------------------
messages = st.session_state.chat_sessions[st.session_state.active_chat]

for msg in messages:
    cls = "user" if msg["role"] == "user" else "bot"
    icon = "🧑" if msg["role"] == "user" else "🤖"
    st.markdown(
        f"<div class='chat-msg {cls}'>{icon} {msg['content']}</div>",
        unsafe_allow_html=True
    )

# -------------------------------------------------
# CHAT INPUT
# -------------------------------------------------
user_prompt = st.chat_input("Ask something…")

if user_prompt:
    messages.append({"role": "user", "content": user_prompt})
    with st.spinner("Thinking…"):
        time.sleep(0.35)
        reply = generate_reply(user_prompt)
    messages.append({"role": "assistant", "content": reply})
    st.rerun()

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("""
<div class="footer">
🤖 This assistant supports project explanation, dataset understanding,
model interpretation, and file-based Q&A.<br>
© 2026 Groundwater Intelligence Platform
</div>
""", unsafe_allow_html=True)
