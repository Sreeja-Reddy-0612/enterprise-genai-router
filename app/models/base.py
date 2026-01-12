from abc import ABC, abstractmethod
from app.core.task import Task
from app.core.response import ModelResponse

class BaseModel(ABC):
    """
    Abstract base class for all AI model providers.
    Ensures a consistent execution interface.
    """

    @abstractmethod
    def generate(self, task: Task) -> ModelResponse:
        pass
