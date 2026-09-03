import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class HoneyCompany(Base):
    __tablename__ = "honey_companies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Core info
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    domain: Mapped[str | None] = mapped_column(String(255))
    region: Mapped[str | None] = mapped_column(String(100))
    company_type: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)

    # Export readiness
    export_tier: Mapped[str | None] = mapped_column(String(50))
    marketplace_status: Mapped[str | None] = mapped_column(String(200))
    estimated_employees: Mapped[str | None] = mapped_column(String(50))

    # India relevance scoring
    india_fit_score: Mapped[float | None] = mapped_column(Float)
    product_market_fit: Mapped[float | None] = mapped_column(Float)
    premium_positioning: Mapped[float | None] = mapped_column(Float)
    export_readiness: Mapped[float | None] = mapped_column(Float)
    production_scale: Mapped[float | None] = mapped_column(Float)
    manuka_exposure: Mapped[float | None] = mapped_column(Float)
    operational_readiness: Mapped[float | None] = mapped_column(Float)

    # Relationships
    contacts: Mapped[list["Contact"]] = relationship(back_populates="honey_company", cascade="all, delete-orphan")
    products: Mapped[list["HoneyProduct"]] = relationship(back_populates="honey_company", cascade="all, delete-orphan")
    opportunities: Mapped[list["Opportunity"]] = relationship(back_populates="honey_company", cascade="all, delete-orphan")
    trade_flows: Mapped[list["TradeFlow"]] = relationship(back_populates="honey_company")
    research_reports: Mapped[list["ResearchReport"]] = relationship(back_populates="honey_company")
