from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class EnrichedContact:
    name: str | None = None
    title: str | None = None
    email: str | None = None
    email_confidence: float | None = None
    phone: str | None = None
    source: str = ""


class EnrichmentProvider(ABC):
    @abstractmethod
    def find_contacts(self, domain: str, *, limit: int = 10) -> list[EnrichedContact]:
        raise NotImplementedError
