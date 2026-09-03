from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.models.intelligence import AgentRun, ResearchReport
from src.schemas.intelligence import AgentRunRead, ResearchReportRead

router = APIRouter(prefix="/research", tags=["research"])

AGENT_TYPES = [
    "market_research",
    "buyer_discovery",
    "company_intelligence",
    "trade_intelligence",
    "regulatory",
    "competitive_intelligence",
    "revenue",
    "monitoring",
]


@router.get("/agent-types")
def list_agent_types():
    return AGENT_TYPES


@router.get("/runs", response_model=list[AgentRunRead])
def list_agent_runs(db: Session = Depends(get_db)):
    return db.query(AgentRun).order_by(AgentRun.created_at.desc()).limit(50).all()


@router.get("/reports", response_model=list[ResearchReportRead])
def list_reports(db: Session = Depends(get_db)):
    return db.query(ResearchReport).order_by(ResearchReport.created_at.desc()).limit(50).all()
