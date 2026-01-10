import streamlit as st
import json
import os
import hashlib
import re

# -------------------------------------------------
# PAGE CONFIG (SIDEBAR DISABLED)
# -------------------------------------------------
st.set_page_config(
    page_title="Groundwater Intelligence Platform",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------
# ADMIN MASTER KEY
# -------------------------------------------------
ADMIN_MASTER_KEY = "GW-ADMIN-2026"

# -------------------------------------------------
# PATHS
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

USERS_PATH = os.path.join(DATA_DIR, "users.json")

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def password_is_strong(password: str) -> tuple:
    if len(password) < 8:
        return False, "At least 8 characters required"
    if not re.search(r"[A-Z]", password):
        return False, "Add at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Add at least one lowercase letter"
    if not re.search(r"[0-9]", password):
        return False, "Add at least one number"
    if not re.search(r"[^A-Za-z0-9]", password):
        return False, "Add at least one special character"
    return True, ""

def load_users():
    if os.path.exists(USERS_PATH):
        with open(USERS_PATH, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_PATH, "w") as f:
        json.dump(users, f, indent=4)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

if "user" not in st.session_state:
    st.session_state.user = None

if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# -------------------------------------------------
# GLOBAL STYLES (PREMIUM + NO SIDEBAR)
# -------------------------------------------------
st.markdown("""
<style>
/* Force hide sidebar */
section[data-testid="stSidebar"] {
    display: none !important;
}

/* Background */
.stApp {
    background:
        radial-gradient(900px 600px at 20% 18%, rgba(79,195,247,0.22), transparent 45%),
        radial-gradient(900px 600px at 80% 82%, rgba(99,102,241,0.22), transparent 45%),
        linear-gradient(180deg, #020617, #030b1c);
    color: #E5E7EB;
    animation: fadeIn 0.8s ease;
}

/* Fade in */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Main card */
.auth-card {
    background: rgba(11,18,32,0.95);
    border-radius: 24px;
    padding: 42px;
    box-shadow: 0 40px 120px rgba(0,0,0,0.75);
}

/* Headings */
.auth-title {
    font-size: 40px;
    font-weight: 900;
}

.auth-sub {
    font-size: 17px;
    opacity: 0.8;
    margin-bottom: 28px;
}

/* Divider glow */
.divider {
    height: 1px;
    margin: 28px 0;
    background: linear-gradient(90deg, transparent, rgba(79,195,247,0.7), transparent);
}

/* Buttons */
button[kind="primary"] {
    font-size: 16px !important;
    padding: 10px 18px !important;
    box-shadow: 0 0 25px rgba(79,195,247,0.4);
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# AUTH GATE
# -------------------------------------------------
if not st.session_state.is_authenticated:

    st.markdown(
        """
        <div class="auth-card">
            <div class="auth-title">🌊 Groundwater Intelligence</div>
            <div class="auth-sub">
                AI-driven groundwater prediction & decision support platform
            </div>
        """,
        unsafe_allow_html=True
    )

    tabs = st.tabs(["🔐 Login", "📝 Sign Up", "🛠 Admin", "🚀 Demo"])
    users = load_users()

    # ---------------- LOGIN ----------------
    with tabs[0]:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            hashed = hash_password(password)
            if email in users and users[email]["password"] == hashed:
                st.session_state.is_authenticated = True
                st.session_state.user = users[email]
                st.success("Login successful")
                st.page_link("pages/📊 Dashboard.py", label="➡ Go to Dashboard")
            else:
                st.error("Invalid email or password")

    # ---------------- SIGN UP ----------------
    with tabs[1]:
        name = st.text_input("Full Name")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_pass")
        role = st.selectbox("Role", ["Student", "Researcher", "Analyst", "Recruiter"])

        if st.button("Create Account"):
            ok, msg = password_is_strong(password)
            if not ok:
                st.error(f"Weak password: {msg}")
            elif email in users:
                st.error("User already exists")
            elif not name or not email:
                st.warning("All fields are required")
            else:
                users[email] = {
                    "email": email,
                    "password": hash_password(password),
                    "name": name,
                    "role": role
                }
                save_users(users)
                st.success("Account created — you can now log in")

    # ---------------- ADMIN ----------------
    with tabs[2]:
        st.info("Admin access via master key")
        admin_key = st.text_input("Enter Admin Master Key", type="password")

        if st.button("Login as Admin"):
            if admin_key == ADMIN_MASTER_KEY:
                st.session_state.is_authenticated = True
                st.session_state.is_admin = True
                st.session_state.user = {
                    "name": "Admin",
                    "role": "Administrator"
                }
                st.success("Admin access granted")
                st.metric("👥 Total Registered Users", len(users))
                st.page_link("pages/📊 Dashboard.py", label="➡ Go to Dashboard")
            else:
                st.error("Invalid admin key")

    # ---------------- DEMO ----------------
    with tabs[3]:
        st.info("Instant recruiter walkthrough mode")

        if st.button("🚀 Enter Demo Mode"):
            st.session_state.is_authenticated = True
            st.session_state.demo_mode = True
            st.session_state.user = {
                "name": "Demo Recruiter",
                "role": "Recruiter"
            }
            st.page_link("pages/📊 Dashboard.py", label="➡ Launch Demo")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# AUTHENTICATED
# -------------------------------------------------
else:
    st.success(f"Welcome back, {st.session_state.user['name']} 👋")
    st.page_link("pages/📊 Dashboard.py", label="➡ Continue to Dashboard")
