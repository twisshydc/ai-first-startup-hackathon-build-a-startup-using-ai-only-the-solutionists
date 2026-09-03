from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class HoneyCompanyCreate(BaseModel):
    name: str
    domain: str | None = None
    region: str | None = None
    company_type: str | None = None
    description: str | None = None
    export_tier: str | None = None
    marketplace_status: str | None = None


class HoneyCompanyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    domain: str | None
    region: str | None
    company_type: str | None
    export_tier: str | None
    marketplace_status: str | None
    india_fit_score: float | None
    created_at: datetime
