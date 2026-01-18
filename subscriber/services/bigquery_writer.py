from google.cloud import bigquery
from datetime import datetime, date
import json

# BigQuery client
client = bigquery.Client()

# Fully qualified table ID
TABLE_ID = "all-in-one-cloud.employee_audit.events"


def make_json_safe(obj):
    """
    Recursively convert Python objects to JSON-safe values.
    - datetime/date -> ISO 8601 string
    - dict/list -> deep conversion
    """
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    elif isinstance(obj, (datetime, date)):
        return obj.isoformat()
    else:
        return obj


def push_to_bigquery(event_type: str, payload: dict):
    """
    Insert employee event into BigQuery.
    This function MUST NEVER crash the subscriber.
    """
    try:
        # 🔹 Make payload 100% JSON-safe
        safe_payload = make_json_safe(payload)

        # 🔹 BigQuery row
        row = {
            "event_type": event_type,
            "emp_id": safe_payload.get("emp_id"),
            "payload": safe_payload,          # JSON column
            "created_at": datetime.utcnow()   # TIMESTAMP column
        }

        # 🔹 Insert row
        errors = client.insert_rows_json(TABLE_ID, [row])

        if errors:
            print("❌ BigQuery insert error:", errors)
        else:
            print("✅ BigQuery insert success")

    except Exception as e:
        # NEVER crash Pub/Sub subscriber
        print("❌ BigQuery exception:", e)
