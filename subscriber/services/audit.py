from google.cloud import firestore
db = firestore.Client()

def save_audit(event_type, payload):
    db.collection("events").add({
        "type": event_type,
        "payload": payload
    })
