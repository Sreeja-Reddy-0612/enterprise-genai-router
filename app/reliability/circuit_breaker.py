import time

class CircuitBreaker:
    def __init__(self, failure_threshold=3, reset_timeout=30):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure_time = None
        self.open = False

    def record_success(self):
        self.failures = 0
        self.open = False

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.open = True

    def allow_request(self):
        if not self.open:
            return True

        if time.time() - self.last_failure_time > self.reset_timeout:
            self.open = False
            self.failures = 0
            return True

        return False
