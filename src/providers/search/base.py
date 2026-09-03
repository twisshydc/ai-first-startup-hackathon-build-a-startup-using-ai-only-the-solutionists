from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str = ""
    published_at: str | None = None
    raw: dict = field(default_factory=dict)


class SearchProvider(ABC):
    @abstractmethod
    def search(self, query: str, *, max_results: int = 10) -> list[SearchResult]:
        raise NotImplementedError

    @abstractmethod
    def extract(self, url: str) -> str | None:
        raise NotImplementedError
