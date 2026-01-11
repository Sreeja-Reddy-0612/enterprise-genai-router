from openai import OpenAI
from models.base import BaseModel
from core.task import Task
from core.response import ModelResponse
from utils.retry import retry_on_failure
from utils.logger import logger
from config.settings import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

class OpenAIModel(BaseModel):

    @retry_on_failure
    def generate(self, task: Task) -> ModelResponse:
        logger.info("Calling OpenAI model")

        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful enterprise AI assistant."},
                {"role": "user", "content": task.user_input}
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content
        tokens = response.usage.total_tokens

        return ModelResponse(
            content=content,
            model_used="openai",
            tokens_used=tokens,
            cost=tokens * 0.000002,
            policy_trace={}
        )
