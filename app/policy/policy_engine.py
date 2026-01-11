from core.task import Task
from core.decision import PolicyDecision

class PolicyEngine:
    """
    Determines which AI model should handle a task
    based on enterprise policies.
    """

    def evaluate(self, task: Task) -> PolicyDecision:
        safety_actions = []
        fallback_chain = ["openai", "gemini", "claude", "mistral"]

        # 1️⃣ Sensitivity-first policy
        if task.sensitivity == "confidential":
            return PolicyDecision(
                selected_model="mistral",
                reason="Confidential data must remain internal",
                estimated_cost=0.0,
                safety_actions=["no_external_api"],
                fallback_chain=[]
            )

        # 2️⃣ Compliance-first policy
        if task.task_type == "compliance":
            return PolicyDecision(
                selected_model="claude",
                reason="Compliance-sensitive task requires safety-first model",
                estimated_cost=0.02,
                safety_actions=["constitutional_ai"],
                fallback_chain=["openai"]
            )

        # 3️⃣ Multimodal policy
        if task.task_type == "multimodal":
            return PolicyDecision(
                selected_model="gemini",
                reason="Multimodal reasoning required",
                estimated_cost=0.03,
                safety_actions=["vision_guardrails"],
                fallback_chain=["openai"]
            )

        # 4️⃣ Budget-aware fallback
        if task.budget is not None and task.budget < 0.01:
            return PolicyDecision(
                selected_model="mistral",
                reason="Budget constraint triggered local inference",
                estimated_cost=0.0,
                safety_actions=["cost_saving_mode"],
                fallback_chain=[]
            )

        # 5️⃣ Default policy
        return PolicyDecision(
            selected_model="openai",
            reason="Default high-quality reasoning",
            estimated_cost=0.04,
            safety_actions=[],
            fallback_chain=["gemini", "claude"]
        )
