from src.agents.base import BaseAgent


class MarketResearchAgent(BaseAgent):
    """Answers: What is happening in the Indian honey market?
    Which segments are attractive? Which cities? What trends matter?"""

    agent_type = "market_research"

    def run(self, context):
        pass


class BuyerDiscoveryAgent(BaseAgent):
    """Finds importers, distributors, retailers, manufacturers,
    nutraceutical, pharmaceutical, cosmetic, and food companies in India."""

    agent_type = "buyer_discovery"

    def run(self, context):
        pass


class CompanyIntelligenceAgent(BaseAgent):
    """Investigates an individual company and outputs what they do,
    products, scale, locations, existing suppliers, likely demand,
    strategic fit, contacts, and evidence."""

    agent_type = "company_intelligence"

    def run(self, context):
        pass


class TradeIntelligenceAgent(BaseAgent):
    """Investigates import/export data, HS codes, volumes, trade routes,
    pricing, countries of origin, and competitors."""

    agent_type = "trade_intelligence"

    def run(self, context):
        pass


class RegulatoryAgent(BaseAgent):
    """Investigates Indian import requirements, NZ export requirements,
    certifications, labelling, documentation, authorities, and compliance risks."""

    agent_type = "regulatory"

    def run(self, context):
        pass


class CompetitiveIntelligenceAgent(BaseAgent):
    """Investigates competing NZ honey exporters, Indian honey companies,
    international competitors, pricing, positioning, and distribution."""

    agent_type = "competitive_intelligence"

    def run(self, context):
        pass


class RevenueAgent(BaseAgent):
    """Consumes all other intelligence.
    Answers: Who should this NZ honey company sell to, why, and what
    should they do next? Consumes intelligence downstream."""

    agent_type = "revenue"

    def run(self, context):
        pass


class MonitoringAgent(BaseAgent):
    """Continuously watches for changes: new importers, new companies,
    regulations, market changes, competitor activity, trade data, news."""

    agent_type = "monitoring"

    def run(self, context):
        pass
