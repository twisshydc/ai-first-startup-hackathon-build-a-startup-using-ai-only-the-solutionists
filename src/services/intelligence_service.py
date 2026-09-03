from datetime import datetime

from sqlalchemy.orm import Session

from src.models.evidence import Evidence
from src.models.intelligence import AgentRun, ResearchReport


def create_evidence(
    db: Session,
    *,
    claim: str,
    source_url: str | None = None,
    source_title: str | None = None,
    source_type: str | None = None,
    extracted_text: str | None = None,
    confidence: float = 0.0,
    honey_company_id=None,
    indian_company_id=None,
) -> Evidence:
    evidence = Evidence(
        claim=claim,
        source_url=source_url,
        source_title=source_title,
        source_type=source_type,
        extracted_text=extracted_text,
        confidence=confidence,
        retrieved_at=datetime.utcnow(),
        honey_company_id=honey_company_id,
        indian_company_id=indian_company_id,
    )
    db.add(evidence)
    return evidence


def start_agent_run(
    db: Session,
    *,
    agent_type: str,
    input_summary: str | None = None,
) -> AgentRun:
    run = AgentRun(agent_type=agent_type, status="running", input_summary=input_summary)
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def complete_agent_run(db: Session, run: AgentRun, *, output_summary: str | None = None) -> AgentRun:
    run.status = "completed"
    run.completed_at = datetime.utcnow()
    run.output_summary = output_summary
    db.commit()
    db.refresh(run)
    return run


def fail_agent_run(db: Session, run: AgentRun, *, error_message: str) -> AgentRun:
    run.status = "failed"
    run.error_message = error_message
    run.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(run)
    return run


def create_report(
    db: Session,
    *,
    title: str,
    report_type: str,
    content: str | None = None,
    summary: str | None = None,
    honey_company_id=None,
    agent_run_id=None,
) -> ResearchReport:
    report = ResearchReport(
        title=title,
        report_type=report_type,
        content=content,
        summary=summary,
        status="completed",
        honey_company_id=honey_company_id,
        agent_run_id=agent_run_id,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report
