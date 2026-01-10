import streamlit as st
import json
import os
import hashlib
import re
import time

# -------------------------------------------------
# PAGE CONFIG (NO SIDEBAR)
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
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def valid_email(email):
    return re.match(r"^[a-zA-Z0-9._%+-]+@(gmail|yahoo|outlook|hotmail)\.com$", email)

def password_is_strong(password):
    return (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"[0-9]", password) and
        re.search(r"[^A-Za-z0-9]", password)
    )

def load_users():
    if os.path.exists(USERS_PATH):
        with open(USERS_PATH, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_PATH, "w") as f:
        json.dump(users, f, indent=4)

def redirect_with_loader():
    with st.spinner("Launching dashboard..."):
        time.sleep(1.2)
    st.switch_page("pages/📊 Dashboard.py")

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
for k, v in {
    "is_authenticated": False,
    "user": None,
    "is_admin": False,
    "demo_mode": False
}.items():
    st.session_state.setdefault(k, v)

# -------------------------------------------------
# STYLES
# -------------------------------------------------
st.markdown("""
<style>
section[data-testid="stSidebar"] { display: none !important; }

.stApp {
    background:
        radial-gradient(900px 600px at 20% 18%, rgba(79,195,247,0.22), transparent 45%),
        radial-gradient(900px 600px at 80% 82%, rgba(99,102,241,0.22), transparent 45%),
        linear-gradient(180deg, #020617, #030b1c);
    color: #E5E7EB;
}

.auth-card {
    background: rgba(11,18,32,0.96);
    border-radius: 26px;
    padding: 44px;
    box-shadow: 0 45px 140px rgba(0,0,0,0.8);
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# AUTH GATE
# -------------------------------------------------
if not st.session_state.is_authenticated:

    st.markdown("""
    <div class="auth-card">
        <h1>🌊 Groundwater Intelligence</h1>
        <p>AI-driven groundwater prediction & decision support</p>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["🔐 Login", "📝 Sign Up", "🛠 Admin", "🚀 Demo"])
    users = load_users()

    # ---------------- LOGIN ----------------
    with tabs[0]:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

        if submit:
            if email in users and users[email]["password"] == hash_password(password):
                st.session_state.is_authenticated = True
                st.session_state.user = users[email]
                redirect_with_loader()
            else:
                st.error("Invalid credentials")

        st.caption("Forgot password? Contact admin to reset securely.")

    # ---------------- SIGN UP ----------------
    with tabs[1]:
        name = st.text_input("Full Name")
        email = st.text_input("Email (gmail / outlook / yahoo)")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Re-enter Password", type="password")
        role = st.selectbox("Role", ["Student", "Researcher", "Analyst", "Recruiter"])

        if st.button("Create Account"):
            if not valid_email(email):
                st.error("Use a valid email provider (gmail, outlook, yahoo)")
            elif email in users:
                st.error("User already exists")
            elif password != confirm:
                st.error("Passwords do not match")
            elif not password_is_strong(password):
                st.error("Password too weak")
            else:
                users[email] = {
                    "email": email,
                    "password": hash_password(password),
                    "name": name,
                    "role": role
                }
                save_users(users)
                st.session_state.is_authenticated = True
                st.session_state.user = users[email]
                redirect_with_loader()

    # ---------------- ADMIN ----------------
    with tabs[2]:
        key = st.text_input("Admin Master Key", type="password")
        if st.button("Login as Admin"):
            if key == ADMIN_MASTER_KEY:
                st.session_state.is_authenticated = True
                st.session_state.is_admin = True
                st.session_state.user = {"name": "Admin", "role": "Administrator"}
                redirect_with_loader()
            else:
                st.error("Invalid master key")

    # ---------------- DEMO ----------------
    with tabs[3]:
        if st.button("Enter Demo Mode"):
            st.session_state.is_authenticated = True
            st.session_state.demo_mode = True
            st.session_state.user = {"name": "Demo Recruiter", "role": "Recruiter"}
            redirect_with_loader()

    st.markdown("</div>", unsafe_allow_html=True)

else:
    redirect_with_loader()
