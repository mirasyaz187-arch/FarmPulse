import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    # Ia akan baca fail JSON yang dimuat naik dalam GitHub secara terus
    cred = credentials.Certificate(r"c:\python1\FarmPulse_API\farmpulse-76e0firebase-adminsdk-abc123.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()