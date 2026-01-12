import uuid
from app.reliability.model_guard import ModelGuard
from app.models.mock_model import MockModel
from app.utils.logger import logger

from app.models.openai_model import OpenAIModel
from app.models.gemini_model import GeminiModel
from app.models.claude_model import ClaudeModel
from app.models.mistral_model import MistralModel

from app.observability.trace_store import start_trace, add_trace_step
from app.observability.metrics import record_request
from app.observability.audit_logger import log_audit


class ModelRouter:
    def __init__(self):
        self.guard = ModelGuard()

        self.models = {
            "openai": OpenAIModel(),
            "gemini": GeminiModel(),
            "claude": ClaudeModel(),
            "mistral": MistralModel(),
        }

        self.mock = MockModel(name="mock-fallback")

    def execute(self, task, decision):
        request_id = str(uuid.uuid4())
        start_trace(request_id)

        attempted = []
        models_to_try = [decision.selected_model] + decision.fallback_chain

        for model_name in models_to_try:
            if not self.guard.is_healthy(model_name):
                logger.warning(f"Skipping unhealthy model: {model_name}")
                continue

            model = self.models.get(model_name)
            if not model:
                continue

            try:
                logger.info(f"Attempting model: {model_name}")
                response = model.generate(task)

                self.guard.record_success(model_name)
                record_request(model_name, success=True)

                add_trace_step(request_id, {
                    "model": model_name,
                    "status": "success"
                })

                log_audit({
                    "request_id": request_id,
                    "model": model_name,
                    "status": "success"
                })

                response.policy_trace = {
                    "attempted_models": attempted + [model_name],
                    "final_model": model_name,
                    "reason": decision.reason
                }

                return response

            except Exception as e:
                logger.error(f"Model {model_name} failed: {e}")
                attempted.append(model_name)

                self.guard.record_failure(model_name)
                record_request(model_name, success=False)

                add_trace_step(request_id, {
                    "model": model_name,
                    "status": "failed",
                    "error": str(e)
                })

        # 🔥 FINAL GUARANTEED FALLBACK — mock is last guaranteed success
        logger.warning("All real models failed — using mock fallback")

        from app.core.response import ModelResponse

        try:
            response = self.mock.generate(task)
            record_request("mock", success=True)

            add_trace_step(request_id, {
                "model": "mock",
                "status": "fallback"
            })

            response.policy_trace = {
                "attempted_models": attempted,
                "final_model": "mock",
                "reason": "all_models_failed"
            }

            return response

        except Exception as e:
            # Ensure we never raise from the fallback — return a safe response
            logger.error(f"Mock fallback failed unexpectedly: {e}")
            record_request("mock", success=False)

            add_trace_step(request_id, {
                "model": "mock",
                "status": "fallback",
                "error": str(e)
            })

            # Construct a minimal safe ModelResponse and return it — do not raise
            safe_response = ModelResponse(
                content="Mock fallback response (safe) — system recovered.",
                model_used="mock",
                tokens_used=0,
                cost=0.0,
                policy_trace={
                    "attempted_models": attempted,
                    "final_model": "mock",
                    "reason": "mock_failed"
                }
            )

            return safe_response
