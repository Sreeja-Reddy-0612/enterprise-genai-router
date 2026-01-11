# Phase 2 – Policy Engine Implementation

In this phase, I implemented the core policy engine that determines
which GenAI model should handle a given task.

Key design principles:
- Policies are explicit rules, not LLM prompts
- Data sensitivity and compliance are prioritized first
- Model selection is deterministic and explainable
- Cost awareness and fallback strategies are first-class concerns

Policy evaluation order:
1. Data sensitivity (confidential data handled locally)
2. Task type (compliance, multimodal, creative)
3. Budget constraints
4. Default high-quality routing

Outcome:
The system can now make enterprise-grade AI routing decisions
before invoking any external or internal model.
