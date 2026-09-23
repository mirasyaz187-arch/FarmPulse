import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# ==========================================
# FIREBASE CONFIGURATION
# ==========================================

# Semak jika Firebase belum di-initialize untuk elak ralat duplicate app
if not firebase_admin._apps:
    # Ambil terus maklumat daripada Secrets Streamlit Cloud (format TOML)
    firebase_secrets = dict(st.secrets["firebase"])
    cred = credentials.Certificate(firebase_secrets)
    firebase_admin.initialize_app(cred)

db = firestore.client()

print("🔥 Firebase connected successfully!")
print("✅ Firestore is ready!")