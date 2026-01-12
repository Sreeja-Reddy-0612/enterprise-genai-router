from app.core.task import Task
from app.core.decision import PolicyDecision
from app.core.response import ModelResponse

from app.models.openai_model import OpenAIModel
from app.models.gemini_model import GeminiModel
from app.models.claude_model import ClaudeModel
from app.models.mistral_model import MistralModel
from app.utils.logger import logger

from app.observability.audit_logger import log_audit
from app.observability.trace_store import start_trace, add_trace_step
from app.observability.metrics import record_request

import uuid


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
        attempted = []
        request_id = str(uuid.uuid4())

        start_trace(request_id)

        models_to_try = [decision.selected_model] + decision.fallback_chain

        for model_name in models_to_try:
            try:
                logger.info(f"Attempting model: {model_name}")

                model = self.models[model_name]
                response = model.generate(task)

                add_trace_step(request_id, {
                    "model": model_name,
                    "status": "success"
                })

                record_request(model_name, success=True)

                log_audit({
                    "request_id": request_id,
                    "model": model_name,
                    "status": "success"
                })

                response.policy_trace = {
                    "request_id": request_id,
                    "attempted_models": attempted + [model_name],
                    "final_model": model_name
                }

                return response

            except Exception as e:
                attempted.append(model_name)

                add_trace_step(request_id, {
                    "model": model_name,
                    "status": "failed",
                    "error": str(e)
                })

                logger.error(f"Model {model_name} failed", exc_info=e)

        record_request("all", success=False)
        raise RuntimeError("All model attempts failed")
