from core.task import Task
from core.decision import PolicyDecision
from core.response import ModelResponse

from models.openai_model import OpenAIModel
from models.gemini_model import GeminiModel
from models.claude_model import ClaudeModel
from models.mistral_model import MistralModel

class ModelRouter:
    """
    Executes a PolicyDecision by invoking the selected model.
    """

    def __init__(self):
        self.models = {
            "openai": OpenAIModel(),
            "gemini": GeminiModel(),
            "claude": ClaudeModel(),
            "mistral": MistralModel()
        }

    def execute(self, task: Task, decision: PolicyDecision) -> ModelResponse:
        model_name = decision.selected_model

        if model_name not in self.models:
            raise ValueError(f"Unsupported model: {model_name}")

        response = self.models[model_name].generate(task)

        # Attach policy trace for explainability
        response.policy_trace = {
            "selected_model": decision.selected_model,
            "reason": decision.reason,
            "fallback_chain": decision.fallback_chain
        }

        return response
