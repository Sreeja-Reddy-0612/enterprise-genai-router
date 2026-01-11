import requests
from models.base import BaseModel
from core.task import Task
from core.response import ModelResponse
from utils.retry import retry_on_failure
from utils.logger import logger
from config.settings import MISTRAL_BASE_URL, MISTRAL_MODEL

class MistralModel(BaseModel):

    @retry_on_failure
    def generate(self, task: Task) -> ModelResponse:
        logger.info("Calling Mistral (local inference)")

        resp = requests.post(
            f"{MISTRAL_BASE_URL}/api/generate",
            json={
                "model": MISTRAL_MODEL,
                "prompt": task.user_input,
                "stream": False
            },
            timeout=30
        )

        data = resp.json()

        return ModelResponse(
            content=data["response"],
            model_used="mistral",
            tokens_used=0,
            cost=0.0,
            policy_trace={}
        )
