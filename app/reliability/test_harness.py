from app.models.test_models import DeterministicModel
from app.router.model_router import ModelRouter
from app.core.task import Task


def run_reliability_scenarios():
    router = ModelRouter()

    router.register(DeterministicModel("model_a", "fail"))
    router.register(DeterministicModel("model_b", "timeout"))
    router.register(DeterministicModel("model_c", "success"))

    task = Task(
        user_input="compliance test",
        task_type="compliance",
        risk_level="high",
        sensitivity="confidential",
        budget=0.05
    )

    response = router.execute(task)

    return {
        "final_model": response.model_used,
        "output": response.content,
        "policy_trace": response.policy_trace
    }
