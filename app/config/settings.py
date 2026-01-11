import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

REQUEST_TIMEOUT = 20
MAX_RETRIES = 3

MISTRAL_BASE_URL = os.getenv("MISTRAL_BASE_URL", "http://localhost:8000")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-7b-instruct-v0.1")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
