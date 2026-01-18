from google.cloud import bigquery
from datetime import datetime, date
import json

client = bigquery.Client()
TABLE_ID = "all-in-one-cloud.employee_audit.events"


def make_json_safe(obj):
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    elif isinstance(obj, (datetime, date)):
        return obj.isoformat()
    else:
        return obj


def push_to_bigquery(event_type, payload):
    try:
        safe_payload = make_json_safe(payload)

        row = {
            "event_type": event_type,
            "emp_id": payload.get("emp_id"),
            "payload": safe_payload,        # ✅ JSON column
            "created_at": datetime.utcnow() # ✅ TIMESTAMP column
        }

        errors = client.insert_rows_json(TABLE_ID, [row])
        if errors:
            print("❌ BigQuery insert error:", errors)

    except Exception as e:
        print("❌ BigQuery exception:", e)
