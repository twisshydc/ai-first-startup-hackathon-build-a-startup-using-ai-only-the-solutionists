import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class Regulation(Base):
    __tablename__ = "regulations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    authority: Mapped[str | None] = mapped_column(String(255))
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    requirements: Mapped[str | None] = mapped_column(Text)
    relevant_for: Mapped[str | None] = mapped_column(String(100))  # export, import, both
    product_category: Mapped[str | None] = mapped_column(String(100))


class Certification(Base):
    __tablename__ = "certifications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    issuing_body: Mapped[str | None] = mapped_column(String(255))
    country: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    required_for_india: Mapped[bool] = mapped_column(default=False)
    relevant_for: Mapped[str | None] = mapped_column(String(100))


class Tariff(Base):
    __tablename__ = "tariffs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    hs_code: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    origin_country: Mapped[str] = mapped_column(String(100), default="New Zealand")
    destination_country: Mapped[str] = mapped_column(String(100), default="India")
    duty_rate: Mapped[str | None] = mapped_column(String(50))
    additional_duties: Mapped[str | None] = mapped_column(String(255))
    gst_rate: Mapped[str | None] = mapped_column(String(50))
    effective_date: Mapped[str | None] = mapped_column(String(50))
    notes: Mapped[str | None] = mapped_column(Text)
