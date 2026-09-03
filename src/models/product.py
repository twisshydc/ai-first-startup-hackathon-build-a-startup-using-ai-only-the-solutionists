import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class HoneyProduct(Base):
    __tablename__ = "honey_products"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Core info
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    honey_type: Mapped[str | None] = mapped_column(String(100))  # manuka, clover, bush, etc.
    umf_mgo: Mapped[str | None] = mapped_column(String(50))  # UMF/MGO rating for manuka
    grade: Mapped[str | None] = mapped_column(String(50))
    volume_capacity: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)

    # Pricing
    estimated_price_nzd: Mapped[float | None] = mapped_column(Float)
    estimated_price_per_kg: Mapped[float | None] = mapped_column(Float)

    # Certifications
    organic: Mapped[bool] = mapped_column(default=False)
    manuka_certified: Mapped[bool] = mapped_column(default=False)

    # Foreign key
    honey_company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("honey_companies.id")
    )

    # Relationships
    honey_company: Mapped["HoneyCompany"] = relationship(back_populates="products")
