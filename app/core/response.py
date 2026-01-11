from dataclasses import dataclass
from typing import Dict

@dataclass
class ModelResponse:
    content: str
    model_used: str
    tokens_used: int
    cost: float
    policy_trace: Dict
