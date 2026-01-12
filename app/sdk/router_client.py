import requests

class GenAIRouterClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url

    def execute(self, payload: dict):
        res = requests.post(
            f"{self.base_url}/execute",
            json=payload,
            timeout=10
        )
        res.raise_for_status()
        return res.json()
