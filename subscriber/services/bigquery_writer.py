from google.cloud import bigquery
from datetime import datetime

client = bigquery.Client()
TABLE_ID = "all-in-one-cloud.employee_audit.events"

def push_to_bigquery(event_type, payload):
    row = {
        "event_type": event_type,
        "emp_id": payload.get("emp_id"),
        "payload": payload,
        "created_at": datetime.utcnow().isoformat()
    }

    errors = client.insert_rows_json(TABLE_ID, [row])
    if errors:
        print("❌ BigQuery insert error:", errors)
