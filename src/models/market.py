import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class Market(Base):
    __tablename__ = "markets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    gdp: Mapped[str | None] = mapped_column(String(50))
    population: Mapped[str | None] = mapped_column(String(50))
    honey_import_volume: Mapped[str | None] = mapped_column(String(100))
    honey_per_capita: Mapped[str | None] = mapped_column(String(50))


class MarketSegment(Base):
    __tablename__ = "market_segments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    segment_type: Mapped[str] = mapped_column(String(100), nullable=False)  # retail, food_manufacturing, pharmaceutical, cosmetic, nutraceutical
    estimated_size: Mapped[str | None] = mapped_column(String(100))
    growth_rate: Mapped[str | None] = mapped_column(String(50))
    cities: Mapped[str | None] = mapped_column(Text)  # comma-separated list of relevant cities
    relevance_to_nz_honey: Mapped[float | None] = mapped_column(Float)

    # Foreign key
    market_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("markets.id")
    )
