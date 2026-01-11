from core.task import Task
from core.decision import PolicyDecision
from core.response import ModelResponse

def sanity_check():
    task = Task(
        user_input="Summarize internal compliance document",
        task_type="compliance",
        risk_level="high",
        sensitivity="confidential",
        budget=0.05
    )

    decision = PolicyDecision(
        selected_model="claude",
        reason="Compliance-sensitive task",
        estimated_cost=0.02,
        safety_actions=["redaction"],
        fallback_chain=["openai"]
    )

    response = ModelResponse(
        content="Summary text",
        model_used="claude",
        tokens_used=320,
        cost=0.018,
        policy_trace={"rule": "compliance_first"}
    )

    print("✅ Task:", task)
    print("✅ Decision:", decision)
    print("✅ Response:", response)

if __name__ == "__main__":
    sanity_check()
