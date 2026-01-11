from models.base import BaseModel
from core.task import Task
from core.response import ModelResponse

class MistralModel(BaseModel):
    def generate(self, task: Task) -> ModelResponse:
        return ModelResponse(
            content="Mistral local response for: " + task.user_input,
            model_used="mistral",
            tokens_used=400,
            cost=0.0,
            policy_trace={}
        )
