import httpx

from src.config import settings
from src.providers.enrichment.base import EnrichedContact, EnrichmentProvider


class HunterProvider(EnrichmentProvider):
    BASE_URL = "https://api.hunter.io/v2"

    def __init__(self) -> None:
        self.api_key = settings.hunter_api_key

    def find_contacts(self, domain: str, *, limit: int = 10) -> list[EnrichedContact]:
        if not self.api_key:
            return []
        params = {"domain": domain, "limit": limit, "api_key": self.api_key}
        resp = httpx.get(f"{self.BASE_URL}/domain-search", params=params, timeout=30)
        if resp.status_code != 200:
            return []
        data = resp.json()
        contacts = []
        for email in data.get("data", {}).get("emails", []):
            first = email.get("first_name")
            last = email.get("last_name")
            full = f"{first} {last}".strip() if first or last else None
            contacts.append(
                EnrichedContact(
                    name=full,
                    title=email.get("position"),
                    email=email.get("value"),
                    email_confidence=email.get("score"),
                    phone=email.get("phone"),
                    source="hunter",
                )
            )
        return contacts
