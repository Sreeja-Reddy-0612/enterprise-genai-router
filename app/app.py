from tests.contract_checks import sanity_check
from policy.policy_engine import PolicyEngine
from core.task import Task
from router.model_router import ModelRouter

## Phase 2: Policy Engine Test
def policy_test():
    engine = PolicyEngine()

    task = Task(
        user_input="Review internal compliance document",
        task_type="compliance",
        risk_level="high",
        sensitivity="public",
        budget=0.05
    )

    decision = engine.evaluate(task)
    print("\n🧠 Policy Decision:")
    print(decision)

## Phase 3: Full Execution Test
def full_execution_test():
    task = Task(
        user_input="Summarize internal compliance document",
        task_type="compliance",
        risk_level="high",
        sensitivity="public",
        budget=0.05
    )

    policy_engine = PolicyEngine()
    router = ModelRouter()

    decision = policy_engine.evaluate(task)
    response = router.execute(task, decision)

    print("\n🚀 Final Model Response:")
    print(response)

def phase_5_test():
    tasks = [
        Task("Check legal compliance of this policy", "compliance", "high", "public"),
        Task("Explain this architecture diagram", "multimodal", "medium", "public"),
        Task("Summarize internal HR doc", "summarize", "high", "confidential"),
    ]

    policy = PolicyEngine()
    router = ModelRouter()

    for t in tasks:
        d = policy.evaluate(t)
        r = router.execute(t, d)
        print("\n---")
        print("Task:", t.task_type)
        print("Model:", r.model_used)
        print("Output:", r.content[:120])

if __name__ == "__main__":
    sanity_check()
    policy_test()
    full_execution_test()
    phase_5_test()
