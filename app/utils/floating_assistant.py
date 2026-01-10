import streamlit as st

def render_floating_assistant(page: str):
    help_text = {
        "dashboard": (
            "📊 **Dashboard Guide**\n\n"
            "• Visualize groundwater trends\n"
            "• Identify stress & recovery patterns\n"
            "• Built for decision support"
        ),
        "predict": (
            "🔮 **Prediction Guide**\n\n"
            "• Predict groundwater depth below surface\n"
            "• Lower value → safer water level\n"
            "• Higher value → stressed groundwater\n"
            "• Use as guidance, not a sensor"
        ),
        "learn": (
            "📘 **Learn Guide**\n\n"
            "• Why groundwater matters\n"
            "• Dataset & feature meanings\n"
            "• Model logic, limits & future scope"
        )
    }

    # ---------- SIDEBAR STYLES ----------
    st.sidebar.markdown("""
    <style>
    .assistant-bubble {
        position: fixed;
        bottom: 24px;
        left: 18px;
        width: 200px;
        z-index: 9999;
    }

    .assistant-bubble button {
        width: 100%;
        border-radius: 16px;
        background: linear-gradient(
            135deg,
            rgba(79,195,247,0.35),
            rgba(15,23,42,0.95)
        );
        box-shadow: 0 0 25px rgba(79,195,247,0.45);
        font-size: 15px;
        padding: 12px;
        transition: all 0.3s ease;
        border: none;
    }

    .assistant-bubble button:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 40px rgba(79,195,247,0.75);
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------- BUBBLE ----------
    st.sidebar.markdown("<div class='assistant-bubble'>", unsafe_allow_html=True)
    with st.sidebar.popover("🤖 Assistant"):
        st.markdown(help_text.get(page, "Assistant help"))
        st.caption("Context-aware quick help")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
