import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class DataSource(Base):
    __tablename__ = "data_sources"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)  # web, api, government, report, manual
    url: Mapped[str | None] = mapped_column(String(1000))
    description: Mapped[str | None] = mapped_column(Text)
    reliability: Mapped[str | None] = mapped_column(String(50))  # high, medium, low
    last_accessed: Mapped[datetime | None] = mapped_column(DateTime)

    # Relationships
    evidence: Mapped[list["Evidence"]] = relationship(back_populates="data_source")


class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # The claim being supported
    claim: Mapped[str] = mapped_column(Text, nullable=False)
    claim_type: Mapped[str | None] = mapped_column(String(100))  # company_fact, market_data, trade_data, regulatory, contact

    # Source information
    source_url: Mapped[str | None] = mapped_column(String(1000))
    source_title: Mapped[str | None] = mapped_column(String(500))
    source_type: Mapped[str | None] = mapped_column(String(50))  # website, report, government_database, news, etc.

    # Timing
    retrieved_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    published_at: Mapped[datetime | None] = mapped_column(DateTime)

    # Content
    extracted_text: Mapped[str | None] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)

    # Foreign keys
    data_source_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("data_sources.id")
    )
    honey_company_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("honey_companies.id")
    )
    indian_company_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("indian_companies.id")
    )

    # Relationships
    data_source: Mapped["DataSource | None"] = relationship(back_populates="evidence")
