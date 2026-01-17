from google.cloud import pubsub_v1
import json

PROJECT_ID = "all-in-one-cloud"
TOPIC_ID = "employee-events"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

def publish_event(event_type: str, payload: dict):
    message = {
        "event_type": event_type,
        "payload": payload
    }
    publisher.publish(topic_path, json.dumps(message).encode("utf-8"))
