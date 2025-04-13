import streamlit as st

# -------- Page configuration --------
st.set_page_config(page_title="Home", page_icon="🏠", layout="centered")

# -------- Redirect to login if not authenticated --------
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("You must log in first.")
    st.page_link("pages/3_Login.py", label="Go to Login Page 🔐")
    st.stop()

# -------- Title and welcome message --------
st.markdown("<h1 style='text-align: center;'>🏠 Secure Encryptor</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 18px;'>Welcome, {st.session_state.username}!</p>", unsafe_allow_html=True)

# -------- For multiple failed attempts --------
if "locked" not in st.session_state:
    st.session_state.locked = False
    
if st.session_state.locked:
    st.error("Too many failed attempts! Please reauthorize from Login Page.")
    st.page_link("pages/3_Login.py", label="Go to Login Page 🔐")
    st.stop()

# -------- Spacing --------
st.markdown("---")

# -------- Navigation --------
col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])

with col2:
    st.page_link("pages/1_Insert_Data.py", label="🗂️ Insert Data")

with col4:
    st.page_link("pages/2_Retrieve_Data.py", label="🗂️ Retrieve Data")

# -------- Footer --------
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 14px; color: gray;'>Built with love and Streamlit</p>", unsafe_allow_html=True)
