import time
from app.core.response import ModelResponse

class MockModel:
    def __init__(self, name="mock", fail=False, latency=0.1):
        self.name = name
        self.fail = fail
        self.latency = latency

    def generate(self, task):
        time.sleep(self.latency)

        return ModelResponse(
            model_used="mock",
            content="Mock response used because all real models failed.",
            tokens_used=0,
            cost=0.0,
            policy_trace={
                "source": "mock",
                "reason": "fallback"
            }
        )
