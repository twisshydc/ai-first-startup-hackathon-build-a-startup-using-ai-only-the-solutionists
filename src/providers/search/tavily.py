from tavily import TavilyClient

from src.config import settings
from src.providers.search.base import SearchProvider, SearchResult


class TavilyProvider(SearchProvider):
    def __init__(self) -> None:
        self.client = TavilyClient(api_key=settings.tavily_api_key)

    def search(self, query: str, *, max_results: int = 10) -> list[SearchResult]:
        resp = self.client.search(query=query, max_results=max_results)
        results = []
        for item in resp.get("results", []):
            results.append(
                SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    snippet=item.get("content", ""),
                    published_at=item.get("published_date"),
                    raw=item,
                )
            )
        return results

    def extract(self, url: str) -> str | None:
        resp = self.client.extract(urls=[url])
        results = resp.get("results", [])
        if not results:
            return None
        return results[0].get("raw_content")
