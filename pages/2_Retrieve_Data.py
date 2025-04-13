import streamlit as st
import hashlib
from utils import load_data
import base64
from cryptography.fernet import Fernet

# -------- Page configuration --------
st.set_page_config(page_title="Retrieve Data", page_icon="🔓")

# -------- Redirect to login if not authenticated --------
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("You must log in first.")
    st.page_link("pages/3_Login.py", label="Go to Login Page 🔐")
    st.stop()

# -------- Hashing --------
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# -------- Load Stored Data --------
if "stored_data" not in st.session_state:
    st.session_state.stored_data = load_data()

# -------- Initialize Session State --------
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

if "locked" not in st.session_state:
    st.session_state.locked = False  # Initialize locked state as False (not locked)

st.title("🔓 Retrieve Your Secret")

# -------- For multiple failed attempts --------
if st.session_state.locked:
    st.error("Too many failed attempts! Please reauthorize from Login Page.")
    st.page_link("pages/3_Login.py", label="Go to Login Page 🔐")
    st.stop()

# -------- Userinputs --------
username = st.text_input("Enter your name: ")
passkey = st.text_input("Enter your passkey:", type="password")

# -------- Decrypt passkey --------
if st.button("Decrypt Data"):
    all_data = st.session_state.stored_data
    if username not in all_data:
        st.error("Incorrect username or passkey!")
        st.session_state.failed_attempts += 1
    else:
        user_data = all_data[username]
        hashed_input = hash_passkey(passkey)
        
        if hashed_input == user_data["hashed_passkey"]:
            try:
                fernet_key = user_data.get("fernet_key")
                if not fernet_key:
                    st.error("Encryption key missing for this user.")
                    st.stop()
                    
                f = Fernet(fernet_key.encode())  # Convert string back to bytes
                encrypted = base64.b64decode(user_data["encrypted_data"])
                decrypted = f.decrypt(encrypted).decode()
                st.success(f"Your secret is: {decrypted}")
                st.session_state.failed_attempts = 0
            except:
                st.session_state.failed_attempts += 1
                st.error("Incorrect username or passkey!")
        else:
            st.session_state.failed_attempts += 1
            st.error("Incorrect username or passkey!")

    if st.session_state.failed_attempts >= 3:
        st.session_state.locked = True
