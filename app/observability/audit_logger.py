import json
import uuid
from datetime import datetime

AUDIT_LOG_FILE = "artifacts/audit_log.jsonl"

def log_audit(event: dict):
    event["event_id"] = str(uuid.uuid4())
    event["timestamp"] = datetime.utcnow().isoformat()

    with open(AUDIT_LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")

    return event["event_id"]
