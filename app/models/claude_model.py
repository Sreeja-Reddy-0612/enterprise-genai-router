from anthropic import Anthropic
from models.base import BaseModel
from core.task import Task
from core.response import ModelResponse
from utils.retry import retry_on_failure
from utils.logger import logger
from config.settings import ANTHROPIC_API_KEY

client = Anthropic(api_key=ANTHROPIC_API_KEY)

class ClaudeModel(BaseModel):

    @retry_on_failure
    def generate(self, task: Task) -> ModelResponse:
        logger.info("Calling Claude (compliance-safe model)")

        msg = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": task.user_input}
            ]
        )

        text = msg.content[0].text
        tokens = msg.usage.input_tokens + msg.usage.output_tokens

        return ModelResponse(
            content=text,
            model_used="claude",
            tokens_used=tokens,
            cost=tokens * 0.000003,
            policy_trace={}
        )
