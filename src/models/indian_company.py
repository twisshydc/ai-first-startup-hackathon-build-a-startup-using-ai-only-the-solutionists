import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class IndianCompany(Base):
    __tablename__ = "indian_companies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Core info
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    domain: Mapped[str | None] = mapped_column(String(255))
    city: Mapped[str | None] = mapped_column(String(100))
    state: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)

    # Company type (buyer, distributor, importer, retailer, manufacturer)
    company_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # Can be comma-separated: "importer,distributor"

    # Business details
    estimated_revenue: Mapped[str | None] = mapped_column(String(50))
    estimated_employees: Mapped[str | None] = mapped_column(String(50))
    honey_category_active: Mapped[bool] = mapped_column(default=False)
    existing_nz_imports: Mapped[bool] = mapped_column(default=False)

    # Scoring
    buyer_score: Mapped[float | None] = mapped_column(Float)
    relevance_score: Mapped[float | None] = mapped_column(Float)
    product_fit: Mapped[float | None] = mapped_column(Float)
    purchasing_capability: Mapped[float | None] = mapped_column(Float)
    distribution_footprint: Mapped[float | None] = mapped_column(Float)
    premium_compatibility: Mapped[float | None] = mapped_column(Float)
    evidence_quality: Mapped[float | None] = mapped_column(Float)

    # Relationships
    contacts: Mapped[list["Contact"]] = relationship(back_populates="indian_company", cascade="all, delete-orphan")
    trade_flows: Mapped[list["TradeFlow"]] = relationship(back_populates="indian_company")
    opportunities_as_target: Mapped[list["Opportunity"]] = relationship(
        back_populates="indian_company", foreign_keys="Opportunity.indian_company_id"
    )
