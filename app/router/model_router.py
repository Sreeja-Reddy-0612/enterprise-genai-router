from core.task import Task
from core.decision import PolicyDecision
from core.response import ModelResponse

from models.openai_model import OpenAIModel
from models.gemini_model import GeminiModel
from models.claude_model import ClaudeModel
from models.mistral_model import MistralModel
from utils.logger import logger


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
    

    def execute(self, task, decision):
        attempted = []

        models_to_try = [decision.selected_model] + decision.fallback_chain

        for model_name in models_to_try:
            try:
                logger.info(f"Attempting model: {model_name}")
                model = self.models[model_name]
                response = model.generate(task)

                response.policy_trace = {
                    "attempted_models": attempted + [model_name],
                    "final_model": model_name,
                    "reason": decision.reason
                }

                return response

            except Exception as e:
                logger.error(f"Model {model_name} failed: {str(e)}")
                attempted.append(model_name)

        raise RuntimeError("All model attempts failed")
    