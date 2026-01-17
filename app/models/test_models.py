class DeterministicModel:
    def __init__(self, name: str, behavior: str):
        """
        behavior:
          - success
          - fail
          - timeout
          - slow
        """
        self.name = name
        self.behavior = behavior

    def generate(self, prompt: str) -> str:
        if self.behavior == "success":
            return f"{self.name} success response"

        if self.behavior == "fail":
            raise RuntimeError(f"{self.name} forced failure")

        if self.behavior == "timeout":
            raise TimeoutError(f"{self.name} forced timeout")

        if self.behavior == "slow":
            import time
            time.sleep(3)
            return f"{self.name} slow response"

        raise ValueError("Unknown behavior")
