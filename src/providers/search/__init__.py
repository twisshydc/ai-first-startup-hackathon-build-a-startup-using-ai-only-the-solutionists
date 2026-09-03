from src.config import settings
from src.providers.search.base import SearchProvider
from src.providers.search.tavily import TavilyProvider


def get_search_provider() -> SearchProvider:
    if settings.tavily_api_key:
        return TavilyProvider()
    raise RuntimeError(
        "No search provider configured. Set TAVILY_API_KEY in your environment."
    )
