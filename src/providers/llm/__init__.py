from src.config import settings
from src.providers.llm.base import LLMProvider
from src.providers.llm.openai_provider import OpenAIProvider


def get_llm_provider() -> LLMProvider:
    if settings.openai_api_key:
        return OpenAIProvider()
    # Future: add other providers here
    raise RuntimeError(
        "No LLM provider configured. Set OPENAI_API_KEY in your environment."
    )
