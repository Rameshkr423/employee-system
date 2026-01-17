from fastapi import FastAPI, Request
import base64, json

from services.audit import save_audit
from services.email import send_email
from services.notify import notify_manager

app = FastAPI()

@app.post("/pubsub/receive")
async def receive_event(request: Request):
    envelope = await request.json()
    message = envelope.get("message", {})
    data = message.get("data")

    if not data:
        return {"status": "ignored"}

    decoded = base64.b64decode(data).decode("utf-8")
    event = json.loads(decoded)

    event_type = event["event_type"]
    payload = event["payload"]

    save_audit(event_type, payload)
    send_email(event_type, payload)
    notify_manager(event_type, payload)

    return {"status": "processed"}  # ACK
