from dataclasses import dataclass
from typing import List

@dataclass
class PolicyDecision:
    selected_model: str
    reason: str
    estimated_cost: float
    safety_actions: List[str]
    fallback_chain: List[str]
