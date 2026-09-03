import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class ResearchReport(Base):
    __tablename__ = "research_reports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Report details
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    report_type: Mapped[str] = mapped_column(String(100), nullable=False)
    # market_research, company_intelligence, buyer_discovery, trade_intelligence, regulatory
    content: Mapped[str | None] = mapped_column(Text)
    summary: Mapped[str | None] = mapped_column(Text)

    # Status
    status: Mapped[str] = mapped_column(String(50), default="pending")
    # pending, running, completed, failed

    # Foreign keys
    honey_company_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("honey_companies.id")
    )
    agent_run_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agent_runs.id")
    )

    # Relationships
    honey_company: Mapped["HoneyCompany | None"] = relationship(back_populates="research_reports")
    agent_run: Mapped["AgentRun | None"] = relationship(back_populates="research_reports")


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)

    # Run details
    agent_type: Mapped[str] = mapped_column(String(100), nullable=False)
    # market_research, buyer_discovery, company_intelligence, trade_intelligence,
    # regulatory, competitive, revenue, monitoring
    status: Mapped[str] = mapped_column(String(50), default="running")
    # running, completed, failed

    # Input/Output
    input_summary: Mapped[str | None] = mapped_column(Text)
    output_summary: Mapped[str | None] = mapped_column(Text)
    error_message: Mapped[str | None] = mapped_column(Text)

    # Cost tracking
    tokens_used: Mapped[int | None] = mapped_column(Integer)
    api_calls_made: Mapped[int | None] = mapped_column(Integer)
    estimated_cost_usd: Mapped[float | None] = mapped_column(Float)

    # Relationships
    research_reports: Mapped[list["ResearchReport"]] = relationship(back_populates="agent_run")
