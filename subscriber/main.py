from google.cloud import pubsub_v1
import json
from google.cloud import firestore

PROJECT_ID = "all-in-one-cloud"
SUB_ID = "employee-events-sub"

db = firestore.Client()

def callback(message):
    data = json.loads(message.data.decode())

    event = {
        "type": data.get("event_type"),
        "payload": data.get("payload")
    }

    db.collection("events").add(event)

    print("Event received:", event["type"])
    message.ack()

subscriber = pubsub_v1.SubscriberClient()
sub_path = subscriber.subscription_path(PROJECT_ID, SUB_ID)

streaming_pull_future = subscriber.subscribe(sub_path, callback)

print("Subscriber running... (Press CTRL+C to stop)")

# 🔥 THIS LINE KEEPS THE PROCESS ALIVE
try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
    print("Subscriber stopped")
