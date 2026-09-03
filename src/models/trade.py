import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class TradeFlow(Base):
    __tablename__ = "trade_flows"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Trade details
    hs_code: Mapped[str | None] = mapped_column(String(20))
    product_description: Mapped[str | None] = mapped_column(String(255))
    volume_tonnes: Mapped[float | None] = mapped_column(Float)
    value_usd: Mapped[float | None] = mapped_column(Float)
    year: Mapped[int | None] = mapped_column(Integer)
    origin_country: Mapped[str] = mapped_column(String(100), default="New Zealand")
    destination_country: Mapped[str] = mapped_column(String(100), default="India")
    trade_route: Mapped[str | None] = mapped_column(String(255))

    # Foreign keys
    honey_company_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("honey_companies.id")
    )
    indian_company_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("indian_companies.id")
    )

    # Relationships
    honey_company: Mapped["HoneyCompany | None"] = relationship(back_populates="trade_flows")
    indian_company: Mapped["IndianCompany | None"] = relationship(back_populates="trade_flows")


class Competitor(Base):
    __tablename__ = "competitors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    country: Mapped[str | None] = mapped_column(String(100))
    company_type: Mapped[str | None] = mapped_column(String(100))  # nz_exporter, indian_importer, international
    description: Mapped[str | None] = mapped_column(Text)
    estimated_volume: Mapped[str | None] = mapped_column(String(100))
    positioning: Mapped[str | None] = mapped_column(String(255))
    distribution: Mapped[str | None] = mapped_column(Text)
