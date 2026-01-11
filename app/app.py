from tests.contract_checks import sanity_check
from policy.policy_engine import PolicyEngine
from core.task import Task

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

if __name__ == "__main__":
    sanity_check()
    policy_test()
