class MockModel:
    name = "mock"

    def generate(self, prompt: str) -> str:
        return "Mock response used because all real models failed."
