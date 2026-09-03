from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class LLMResponse:
    text: str
    usage: dict = field(default_factory=dict)
    raw: object | None = None


class LLMProvider(ABC):
    @abstractmethod
    def complete(self, system: str, user: str, *, temperature: float = 0.2) -> LLMResponse:
        raise NotImplementedError

    @abstractmethod
    def complete_json(self, system: str, user: str, *, temperature: float = 0.0) -> dict:
        raise NotImplementedError
