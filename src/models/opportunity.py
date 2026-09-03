import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class Opportunity(Base):
    __tablename__ = "opportunities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Opportunity details
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    stage: Mapped[str] = mapped_column(String(50), default="identified")
    # identified, researched, contacted, negotiating, closed_won, closed_lost

    # Scoring
    score: Mapped[float | None] = mapped_column(Float)
    buying_hypothesis: Mapped[str | None] = mapped_column(Text)
    reason_for_fit: Mapped[str | None] = mapped_column(Text)

    # Foreign keys
    honey_company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("honey_companies.id")
    )
    indian_company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("indian_companies.id")
    )

    # Relationships
    honey_company: Mapped["HoneyCompany"] = relationship(back_populates="opportunities")
    indian_company: Mapped["IndianCompany"] = relationship(
        back_populates="opportunities_as_target", foreign_keys=[indian_company_id]
    )
    recommendations: Mapped[list["Recommendation"]] = relationship(back_populates="opportunity", cascade="all, delete-orphan")
    outreach: Mapped[list["Outreach"]] = relationship(back_populates="opportunity", cascade="all, delete-orphan")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Recommendation details
    recommendation_type: Mapped[str] = mapped_column(String(100), nullable=False)
    # next_action, contact_strategy, market_entry, product_fit, pricing
    content: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[str] = mapped_column(String(20), default="medium")
    # high, medium, low

    # Foreign key
    opportunity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("opportunities.id")
    )

    # Relationships
    opportunity: Mapped["Opportunity"] = relationship(back_populates="recommendations")
