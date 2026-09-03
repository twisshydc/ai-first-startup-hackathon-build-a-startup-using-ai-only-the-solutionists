from src.agents.base import BaseAgent, AgentContext
from src.agents.specialized import (
    BuyerDiscoveryAgent,
    CompanyIntelligenceAgent,
    CompetitiveIntelligenceAgent,
    MarketResearchAgent,
    MonitoringAgent,
    RegulatoryAgent,
    RevenueAgent,
    TradeIntelligenceAgent,
)

AGENT_REGISTRY = {
    "market_research": MarketResearchAgent,
    "buyer_discovery": BuyerDiscoveryAgent,
    "company_intelligence": CompanyIntelligenceAgent,
    "trade_intelligence": TradeIntelligenceAgent,
    "regulatory": RegulatoryAgent,
    "competitive_intelligence": CompetitiveIntelligenceAgent,
    "revenue": RevenueAgent,
    "monitoring": MonitoringAgent,
}


def get_agent(agent_type: str) -> BaseAgent:
    if agent_type not in AGENT_REGISTRY:
        raise ValueError(f"Unknown agent type: {agent_type}")
    return AGENT_REGISTRY[agent_type]()


def get_agent_types() -> list[str]:
    return list(AGENT_REGISTRY.keys())
