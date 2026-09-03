from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class IndianCompanyCreate(BaseModel):
    name: str
    domain: str | None = None
    city: str | None = None
    state: str | None = None
    company_type: str
    description: str | None = None
    honey_category_active: bool = False
    existing_nz_imports: bool = False


class IndianCompanyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    domain: str | None
    city: str | None
    state: str | None
    company_type: str
    description: str | None
    buyer_score: float | None
    created_at: datetime
