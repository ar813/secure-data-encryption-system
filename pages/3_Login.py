# pages/3_Login.py

import streamlit as st

# -------- Page configuration --------
st.set_page_config(page_title="Login", page_icon="🔐")

st.title("🔐 Login")

# -------- Userinputs --------
username = st.text_input("Enter your name:")
password = st.text_input("Enter your password:", type="password")

# -------- Login logic --------
if st.button("Login"):
    if username and password:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.success("Login successful!")
        st.page_link("Home.py", label="Go to Home 🏠", icon="🏠")
    else:
        st.error("Please enter both username and passkey.")
