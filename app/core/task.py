from dataclasses import dataclass
from typing import Literal, Optional

@dataclass
class Task:
    user_input: str
    task_type: Literal["chat", "summarize", "code", "compliance", "multimodal"]
    risk_level: Literal["low", "medium", "high"]
    sensitivity: Literal["public", "internal", "confidential"]
    budget: Optional[float] = None
