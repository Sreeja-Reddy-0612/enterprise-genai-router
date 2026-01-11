from models.base import BaseModel
from core.task import Task
from core.response import ModelResponse

class GeminiModel(BaseModel):
    def generate(self, task: Task) -> ModelResponse:
        return ModelResponse(
            content="Gemini response for: " + task.user_input,
            model_used="gemini",
            tokens_used=600,
            cost=0.03,
            policy_trace={}
        )
