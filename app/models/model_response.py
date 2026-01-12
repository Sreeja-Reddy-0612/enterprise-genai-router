from dataclasses import dataclass
from typing import List

@dataclass
class ModelResponse:
    model_used: str
    content: str
    tokens_used: int
    cost: float
    policy_trace: List[str]
