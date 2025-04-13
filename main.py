from cryptography.fernet import Fernet # pip install cryptography
import hashlib
import streamlit as st

# ---------- Setup Session State ----------
if "key" not in st.session_state:
    st.session_state.key = Fernet.generate_key()
    st.session_state.f = Fernet(st.session_state.key)

if "stored_data" not in st.session_state:
    st.session_state.stored_data = {}

if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0
    
if "locked" not in st.session_state:
    st.session_state.locked = False

# ---------- Hash The Passkey ----------
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# ---------- App Layout ----------
st.set_page_config(page_title="Secure Encryptor", page_icon="🔐", layout="centered")
st.title("🔐 Secure Data Encryption")
st.markdown("Keep your secrets safe in **Secure Data Encryption App** using passkey-based security.")

# ---------- Separator ----------
st.markdown("---")


# ---------- Lock Message ----------
if st.session_state.locked:
    st.warning("Too many failed attempts. Please reload the page to try again.")
    st.stop()

# ---------- Encryption ----------
st.subheader("🔒 Encrypt Your Secret")

passkey_for_encryption = st.text_input("Enter your passkey: ", key="encryption", type="password")
hashed_passkey_for_encryption = hash_passkey(passkey_for_encryption)

data = st.text_input("What do you want to hide: ")

if st.button("Encrypt data"):
    if not passkey_for_encryption or not data:
        st.error("Passkey and data are required!")
    else:
        encrypted = st.session_state.f.encrypt(data.encode()) 
        st.session_state.stored_data["hashed_passkey"] = hashed_passkey_for_encryption
        st.session_state.stored_data["encrypted_data"] = encrypted
        st.success("Data encrypted and stored securely!")
        
# ---------- Separator ----------
st.markdown("---")


# ---------- Decryption ----------
st.subheader("🔓 Decrypt Your Secret")

passkey_for_decryption = st.text_input("Enter your passkey: ", key="decryption", type="password")
hashed_passkey_for_decryption = hash_passkey(passkey_for_decryption)  
 
if st.button("Decrypt data"):
    if "hashed_passkey" not in st.session_state.stored_data:
        st.warning("No data has been encrypted yet.")
    else:
        if st.session_state.stored_data["hashed_passkey"] == hashed_passkey_for_decryption:
            decrypted = st.session_state.f.decrypt(st.session_state.stored_data["encrypted_data"]).decode()  
            st.success(f"Decrypted data: {decrypted}")
            st.session_state.failed_attempts = 0
        else:
            st.session_state.failed_attempts += 1
            st.error("Your passkey is wrong!")
            if st.session_state.failed_attempts > 3:
                st.session_state.locked = True