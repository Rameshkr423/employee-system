from google.cloud import bigquery
from datetime import datetime
import json

client = bigquery.Client()
TABLE_ID = "all-in-one-cloud.employee_audit.events"

def push_to_bigquery(event_type, payload):
    try:
        row = {
            "event_type": event_type,
            "emp_id": payload.get("emp_id"),
            # Ensure valid JSON
            "payload": json.loads(json.dumps(payload)),
            # Proper TIMESTAMP
            "created_at": datetime.utcnow()
        }

        errors = client.insert_rows_json(TABLE_ID, [row])
        if errors:
            print("❌ BigQuery insert error:", errors)

    except Exception as e:
        print("❌ BigQuery exception:", e)
