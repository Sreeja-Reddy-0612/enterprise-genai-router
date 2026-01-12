import uuid
from app.models.mock_model import MockModel
from app.reliability.retry_policy import RetryPolicy
from app.reliability.model_health import get_circuit
from app.observability.metrics import record_request
from app.observability.trace_store import start_trace, add_trace_step
from app.utils.logger import logger


class ModelRouter:
    def __init__(self):
        self.models = []
        self.retry_policy = RetryPolicy()
        self.mock = MockModel()

    def register(self, model):
        self.models.append(model)

    def execute(self, task, decision=None):
        trace_id = getattr(task, "id", str(uuid.uuid4()))
        start_trace(trace_id)

        attempted = []

        for model in self.models:
            breaker = get_circuit(model.name)

            if not breaker.allow_request():
                logger.warning(f"Circuit open, skipping {model.name}")
                continue

            try:
                logger.info(f"Attempting model: {model.name}")
                output = self.retry_policy.run(
                    lambda: model.generate(task.user_input)
                )

                record_request(model.name, success=True)
                breaker.record_success()

                add_trace_step(trace_id, {
                    "model": model.name,
                    "status": "success"
                })

                return self._response(
                    model=model.name,
                    content=output,
                    attempted=attempted
                )

            except Exception as e:
                logger.error(f"Model {model.name} failed: {e}")

                breaker.record_failure()
                record_request(model.name, success=False)

                attempted.append(model.name)
                add_trace_step(trace_id, {
                    "model": model.name,
                    "status": "failed",
                    "error": str(e)
                })

        # Fallback
        add_trace_step(trace_id, {
            "model": "mock",
            "status": "fallback"
        })

        return self._response(
            model="mock",
            content=self.mock.generate(task.user_input),
            attempted=attempted,
            fallback=True
        )

    def _response(self, model, content, attempted, fallback=False):
        return type("Response", (), {
            "model_used": model,
            "content": content,
            "policy_trace": {
                "attempted_models": attempted,
                "final_model": model,
                "reason": "all models failed" if fallback else "success"
            }
        })()
