from abc import ABC, abstractmethod
from core.task import Task
from core.response import ModelResponse

class BaseModel(ABC):
    """
    Abstract base class for all AI model providers.
    Ensures a consistent execution interface.
    """

    @abstractmethod
    def generate(self, task: Task) -> ModelResponse:
        pass
