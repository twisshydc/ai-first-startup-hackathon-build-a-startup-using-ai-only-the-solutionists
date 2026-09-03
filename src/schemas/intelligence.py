from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EvidenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    claim: str
    claim_type: str | None
    source_url: str | None
    source_title: str | None
    source_type: str | None
    retrieved_at: datetime
    confidence: float


class AgentRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    agent_type: str
    status: str
    input_summary: str | None
    output_summary: str | None
    error_message: str | None
    created_at: datetime
    completed_at: datetime | None


class ResearchReportRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    report_type: str
    content: str | None
    summary: str | None
    status: str
    created_at: datetime
