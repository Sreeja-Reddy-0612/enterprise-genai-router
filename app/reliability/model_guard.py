import time
from collections import defaultdict

class ModelGuard:
    def __init__(self, failure_threshold=3, cooldown_seconds=60):
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds

        self.failures = defaultdict(int)
        self.last_failed_at = {}

    def is_healthy(self, model_name: str) -> bool:
        if model_name not in self.last_failed_at:
            return True

        last_fail = self.last_failed_at[model_name]
        if time.time() - last_fail > self.cooldown_seconds:
            # cooldown expired → reset
            self.failures[model_name] = 0
            del self.last_failed_at[model_name]
            return True

        return self.failures[model_name] < self.failure_threshold

    def record_success(self, model_name: str):
        self.failures[model_name] = 0
        self.last_failed_at.pop(model_name, None)

    def record_failure(self, model_name: str):
        self.failures[model_name] += 1
        self.last_failed_at[model_name] = time.time()
