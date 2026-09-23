import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# ========================================
# FIREBASE CONFIGURATION
# ==========================================

if not firebase_admin._apps:
    # Ambil maklumat daripada Secrets Streamlit Cloud
    firebase_secrets = dict(st.secrets["firebase"])
    
    # Pastikan private_key memproses format baris baharu (\n) dengan betul
    if "private_key" in firebase_secrets:
        firebase_secrets["private_key"] = firebase_secrets["private_key"].replace("\\n", "\n")

    cred = credentials.Certificate(firebase_secrets)
    firebase_admin.initialize_app(cred)

db = firestore.client()

print("🔥 Firebase connected successfully!")
print("✅ Firestore is ready!") 