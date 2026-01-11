import google.generativeai as genai
from models.base import BaseModel
from core.task import Task
from core.response import ModelResponse
from utils.retry import retry_on_failure
from utils.logger import logger
from config.settings import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

class GeminiModel(BaseModel):

    @retry_on_failure
    def generate(self, task: Task) -> ModelResponse:
        logger.info("Calling Gemini (multimodal-capable model)")

        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(task.user_input)

        return ModelResponse(
            content=response.text,
            model_used="gemini",
            tokens_used=0,  # Gemini doesn’t expose tokens reliably
            cost=0.03,
            policy_trace={}
        )
