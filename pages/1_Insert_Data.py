import streamlit as st
from cryptography.fernet import Fernet
import hashlib
from utils import save_data, load_data
import base64

st.set_page_config(page_title="Insert Data", page_icon="📝")

# -------- Redirect to login if not authenticated --------
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("You must log in first.")
    st.page_link("pages/3_Login.py", label="Go to Login Page 🔐")
    st.stop()
    
# -------- Session State --------
if "key" not in st.session_state:
    if "fernet_key" not in st.session_state:
        st.session_state.fernet_key = Fernet.generate_key()
    st.session_state.key = st.session_state.fernet_key
    st.session_state.f = Fernet(st.session_state.key)

if "stored_data" not in st.session_state:
    st.session_state.stored_data = load_data()

# -------- Hashing --------
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

st.title("🔒 Insert Your Secret")

# -------- For multiple failed attempts --------
if st.session_state.locked:
    st.error("Too many failed attempts! Please reauthorize from Login Page.")
    st.page_link("pages/3_Login.py", label="Go to Login Page 🔐")
    st.stop()

# -------- Userinputs --------
username = st.text_input("Enter your name: ")
passkey = st.text_input("Enter your passkey:", type="password")
data = st.text_area("What do you want to hide?")

# -------- Encrypt and store all inputs without username --------
if st.button("Encrypt and Store"):
    if not passkey or not data or not username:
        st.error("Passkey and data are required!")
    else:
        encrypted = st.session_state.f.encrypt(data.encode())
        hashed = hash_passkey(passkey)

        # Encode encrypted bytes to base64 string for JSON storage
        encrypted_b64 = base64.b64encode(encrypted).decode()

        all_data = st.session_state.stored_data
        
        all_data[username] = {
            "hashed_passkey": hashed,
            "encrypted_data": encrypted_b64,
            "fernet_key": st.session_state.fernet_key.decode()  # Convert bytes to str
        }
        
        st.session_state.stored_data = all_data
        save_data(all_data)
        st.success("Data encrypted and stored successfully!")
