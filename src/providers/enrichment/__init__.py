from src.config import settings
from src.providers.enrichment.base import EnrichmentProvider
from src.providers.enrichment.hunter import HunterProvider


def get_enrichment_provider() -> EnrichmentProvider | None:
    if settings.hunter_api_key:
        return HunterProvider()
    return None
