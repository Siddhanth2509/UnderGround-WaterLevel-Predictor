import streamlit as st
import pandas as pd
import json
import os
import time
from datetime import datetime
from PIL import Image, ImageFile
if not st.session_state.get("is_authenticated"):
    st.warning("Please log in first.")
    st.page_link("app.py", label="🔐 Go to Login")
    st.stop()

ImageFile.LOAD_TRUNCATED_IMAGES = True

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="User Profile | Groundwater Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.markdown("---")

    # -------------------------------
    # Role badge logic
    # -------------------------------
    is_admin = st.session_state.get("is_admin")
    is_demo = st.session_state.get("demo_mode")

    if is_admin:
        badge = "🛠 ADMIN"
        badge_color = "#F43F5E"
        badge_class = "admin-badge"
        role_explain = "Administrator: full access to users, analytics, and system controls."
    elif is_demo:
        badge = "🧪 DEMO"
        badge_color = "#22D3EE"
        badge_class = "demo-badge"
        role_explain = "Demo mode: limited access for recruiters to explore features safely."
    else:
        badge = "👤 USER"
        badge_color = "#4FC3F7"
        badge_class = "user-badge"
        role_explain = "Standard user: can run predictions, explore learning content, and use the assistant."

    # -------------------------------
    # Styles (hover + pulse)
    # -------------------------------
    st.markdown(
        """
        <style>
        .user-card {
            padding:14px;
            border-radius:14px;
            background:#0b1220;
            box-shadow:0 0 18px rgba(79,195,247,0.35);
            text-align:center;
            margin-bottom:12px;
            transition: all 0.35s ease;
        }
        .user-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 0 32px rgba(79,195,247,0.6);
        }
        .admin-badge {
            animation: pulseAdmin 2.2s infinite;
        }
        @keyframes pulseAdmin {
            0%   { box-shadow: 0 0 0 rgba(244,63,94,0.0); }
            50%  { box-shadow: 0 0 18px rgba(244,63,94,0.9); }
            100% { box-shadow: 0 0 0 rgba(244,63,94,0.0); }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # -------------------------------
    # User card
    # -------------------------------
    st.markdown(
        f"""
        <div class="user-card">
            <strong style="font-size:16px;">
                {st.session_state.user['name']}
            </strong><br>
            <span class="{badge_class}" style="
                display:inline-block;
                margin-top:6px;
                padding:4px 10px;
                border-radius:999px;
                font-size:12px;
                font-weight:600;
                color:{badge_color};
                border:1px solid {badge_color};
            ">
                {badge}
            </span><br>
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
# PATHS
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

PROFILE_PATH = os.path.join(DATA_DIR, "user_profile.json")
AVATAR_PATH = os.path.join(DATA_DIR, "profile_avatar.png")

# -------------------------------------------------
# ACTIVITY LOGGER
# -------------------------------------------------
def log_activity(event):
    if "activity_log" not in st.session_state:
        st.session_state.activity_log = []
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.activity_log.append(f"{timestamp} — {event}")

# -------------------------------------------------
# DEFAULT PROFILE
# -------------------------------------------------
default_profile = {
    "name": "Demo User",
    "role": "Student",
    "phone": "",
    "city": "",
    "address": "",
    "experience": ""
}

# -------------------------------------------------
# LOAD PROFILE
# -------------------------------------------------
if os.path.exists(PROFILE_PATH):
    with open(PROFILE_PATH, "r") as f:
        profile = json.load(f)
else:
    profile = default_profile.copy()

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "session_start" not in st.session_state:
    st.session_state.session_start = time.time()
    log_activity("Session started")

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

if "activity_log" not in st.session_state:
    st.session_state.activity_log = []

# -------------------------------------------------
# AUTO SAVE
# -------------------------------------------------
def autosave():
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=4)
    log_activity("Profile updated")

# -------------------------------------------------
# STYLES (PREDICT SIDEBAR + CINEMATIC PAGE)
# -------------------------------------------------
st.markdown("""
<style>
/* Page background */
.stApp {
    background:
        radial-gradient(900px 600px at 12% 18%, rgba(79,195,247,0.18), transparent 45%),
        radial-gradient(900px 600px at 88% 82%, rgba(99,102,241,0.18), transparent 45%),
        linear-gradient(180deg, #020617, #030b1c);
    color: #E5E7EB;
}

/* === SIDEBAR (MATCHES PREDICT PAGE) === */
section[data-testid="stSidebar"] {
    width: 220px;
    background: #050913;
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] a {
    border-radius: 10px;
    margin: 6px 8px;
    padding: 10px 14px;
    font-size: 14px;
    transition: all 0.3s ease;
}

section[data-testid="stSidebar"] a:hover {
    background: rgba(79,195,247,0.18);
    transform: translateX(6px) scale(1.02);
}

/* Cards */
.card {
    background: rgba(11,18,32,0.92);
    border-radius: 22px;
    padding: 26px;
    box-shadow: 0 18px 55px rgba(0,0,0,0.45);
    margin-bottom: 26px;
    transition: transform 0.45s cubic-bezier(.2,.8,.2,1),
                box-shadow 0.45s cubic-bezier(.2,.8,.2,1);
    backdrop-filter: blur(8px);
}
.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 35px 110px rgba(79,195,247,0.35);
}

/* Avatar */
.avatar {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    object-fit: cover;
    box-shadow: 0 0 45px rgba(79,195,247,0.55);
    transition: transform 0.45s ease, box-shadow 0.45s ease;
}
.avatar:hover {
    transform: scale(1.08);
    box-shadow: 0 0 95px rgba(79,195,247,0.9);
}

/* Floating AI Orb */
.ai-orb {
    position: fixed;
    bottom: 42px;
    right: 42px;
    width: 90px;
    height: 90px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%,
        rgba(79,195,247,0.65),
        rgba(2,6,23,0.95)
    );
    box-shadow:
        0 0 45px rgba(79,195,247,0.6),
        inset 0 0 25px rgba(255,255,255,0.05);
    animation: orbFloat 5.5s ease-in-out infinite,
               orbGlow 3.5s ease-in-out infinite;
    opacity: 0.9;
}

@keyframes orbFloat {
    0% { transform: translateY(0); }
    50% { transform: translateY(-14px); }
    100% { transform: translateY(0); }
}

@keyframes orbGlow {
    0%,100% { box-shadow: 0 0 45px rgba(79,195,247,0.6); }
    50% { box-shadow: 0 0 80px rgba(79,195,247,0.9); }
}

/* Footer */
.footer {
    margin-top: 100px;
    text-align: center;
    opacity: 0.75;
    font-size: 14px;
}
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
st.markdown("## 👤 User Profile")
st.caption("Identity, engagement, and system intelligence")

# -------------------------------------------------
# AVATAR + BASIC INFO
# -------------------------------------------------
left, right = st.columns([1, 2])

with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    try:
        if os.path.exists(AVATAR_PATH):
            st.image(AVATAR_PATH, width=140)
        else:
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=140)
    except:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=140)

    uploaded_img = st.file_uploader("Upload profile picture", type=["png","jpg","jpeg"])
    if uploaded_img:
        try:
            img = Image.open(uploaded_img)
            img.verify()
            img = Image.open(uploaded_img)
            img.save(AVATAR_PATH)
            log_activity("Profile picture updated")
            st.success("Profile picture updated")
            st.rerun()
        except:
            st.error("Invalid image file")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    profile["name"] = st.text_input("Name", profile["name"], on_change=autosave)
    profile["role"] = st.selectbox(
        "Role",
        ["Student", "Researcher", "Analyst", "Recruiter", "Policy Maker"],
        index=["Student","Researcher","Analyst","Recruiter","Policy Maker"].index(profile["role"])
        if profile["role"] in ["Student","Researcher","Analyst","Recruiter","Policy Maker"] else 0,
        on_change=autosave
    )
    profile["city"] = st.text_input("City", profile["city"], on_change=autosave)
    st.success("Profile auto-saved ✓")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# PROFILE INTELLIGENCE
# -------------------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### 🧠 Profile Intelligence")
st.markdown(
    "Your role and experience personalize explanations, demo behavior, "
    "and assistant guidance across the platform."
)
st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# ENGAGEMENT METRICS
# -------------------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### 📈 Engagement Metrics")

minutes_spent = int((time.time() - st.session_state.session_start) / 60)
st.metric("⏱ Minutes Spent (Session)", minutes_spent)
st.metric("🔢 Predictions Made", len(st.session_state.prediction_history))
st.metric("📊 Model Reliability", "High (validated range: 2–5 m)")

st.caption(
    "Reliability is estimated from validation performance. "
    "Ground truth is unavailable at inference time."
)
st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# ACTIVITY TIMELINE
# -------------------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### 🧭 Activity Timeline")

for act in st.session_state.activity_log[-10:]:
    st.markdown(f"- {act}")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# FLOATING AI ORB
# -------------------------------------------------
st.markdown("<div class='ai-orb'></div>", unsafe_allow_html=True)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("""
<div class="footer">
👤 Profile with real activity tracking, auto-save & cinematic UX<br>
© 2026 Groundwater Intelligence Platform
</div>
""", unsafe_allow_html=True)
