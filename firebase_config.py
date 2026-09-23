import firebase_admin
from firebase_admin import credentials, firestore


# ==========================================
# FIREBASE CONFIGURATION
# ==========================================

cred = credentials.Certificate("c:\\python1\\FarmPulse_API\\farmpulse-76e0firebase-adminsdk-abc123.json")

firebase_admin.initialize_app(cred)

db = firestore.client()

print("🔥 Firebase connected successfully!")
print("✅ Firestore is ready!")