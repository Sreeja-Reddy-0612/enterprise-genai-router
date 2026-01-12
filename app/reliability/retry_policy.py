import time

class RetryPolicy:
    def __init__(self, retries=2, backoff=1.5):
        self.retries = retries
        self.backoff = backoff

    def run(self, fn):
        last_error = None
        for attempt in range(self.retries + 1):
            try:
                return fn()
            except Exception as e:
                last_error = e
                time.sleep(self.backoff ** attempt)
        raise last_error
