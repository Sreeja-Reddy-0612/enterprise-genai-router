import requests

payload = {
    "user_input": "Summarize internal compliance document",
    "task_type": "compliance",
    "risk_level": "high",
    "sensitivity": "confidential",
    "budget": 0.05
}

requests.post("http://127.0.0.1:8000/execute", json=payload)
