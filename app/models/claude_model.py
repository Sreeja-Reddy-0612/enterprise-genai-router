from models.base import BaseModel
from core.task import Task
from core.response import ModelResponse

class ClaudeModel(BaseModel):
    def generate(self, task: Task) -> ModelResponse:
        return ModelResponse(
            content="Claude response for: " + task.user_input,
            model_used="claude",
            tokens_used=450,
            cost=0.02,
            policy_trace={}
        )
