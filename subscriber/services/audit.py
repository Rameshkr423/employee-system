from google.cloud import firestore
from datetime import datetime

db = firestore.Client()

def save_audit(event_type, payload):
    db.collection("events").add({
        "event_type": event_type,
        "payload": payload,
        "created_at": datetime.utcnow()
    })
