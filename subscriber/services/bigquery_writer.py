from google.cloud import bigquery
from datetime import datetime, date
import json

client = bigquery.Client()
TABLE_ID = "all-in-one-cloud.employee_audit.events"


def make_json_safe(obj):
    """
    Convert Python objects to JSON-safe values
    """
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    elif isinstance(obj, (datetime, date)):
        return obj.isoformat()
    else:
        return obj


def push_to_bigquery(event_type: str, payload):
    """
    FINAL, SAFE BigQuery insert
    - Handles Pub/Sub string payload
    - Handles datetime
    - Never crashes subscriber
    """
    try:
        # 🔥 CRITICAL FIX: Pub/Sub may send payload as STRING
        if isinstance(payload, str):
            payload = json.loads(payload)

        # Make payload fully JSON-safe
        safe_payload = make_json_safe(payload)

        row = {
            "event_type": event_type,
            "emp_id": safe_payload.get("emp_id"),
            "payload": safe_payload,                     # JSON column
            "created_at": datetime.utcnow().isoformat()
        }

        errors = client.insert_rows_json(
            TABLE_ID,
            [row],
            ignore_unknown_values=True
        )

        if errors:
            print("❌ BigQuery insert error:", errors)
        else:
            print("✅ BigQuery insert success")

    except Exception as e:
        # NEVER crash Pub/Sub subscriber
        print("❌ BigQuery exception:", str(e))
