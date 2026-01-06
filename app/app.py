import streamlit as st

st.set_page_config(
    page_title="Groundwater Intelligence Platform",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Redirect message (Dashboard loads automatically)
st.markdown(
    """
    <meta http-equiv="refresh" content="0; url=/Dashboard">
    """,
    unsafe_allow_html=True
)
