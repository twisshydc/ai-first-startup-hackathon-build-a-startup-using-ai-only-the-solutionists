from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class AgentContext:
    """Shared context passed to agents during a run."""
    honey_company_id: UUID | None = None
    indian_company_id: UUID | None = None
    target_country: str = "India"
    market: str = "honey"
    run_id: UUID | None = None
    extra: dict = field(default_factory=dict)


@dataclass
class AgentResult:
    """Structured output from an agent run."""
    agent_type: str
    summary: str
    findings: list = field(default_factory=list)
    evidence: list = field(default_factory=list)
    recommendations: list = field(default_factory=list)
    data: dict = field(default_factory=dict)


class BaseAgent(ABC):
    """Base class for all specialized agents.

    Agents are intentionally modular and independently testable.
    Each agent produces structured output with evidence references.
    """

    agent_type: str = "base"

    def __init__(self, *, llm=None, search=None) -> None:
        self._llm = llm
        self._search = search

    @property
    def llm(self):
        if self._llm is None:
            from src.providers.llm import get_llm_provider

            self._llm = get_llm_provider()
        return self._llm

    @property
    def search(self):
        if self._search is None:
            from src.providers.search import get_search_provider

            self._search = get_search_provider()
        return self._search

    @abstractmethod
    def run(self, context: AgentContext) -> AgentResult:
        raise NotImplementedError

    def _system_prompt(self) -> str:
        return (
            "You are a specialized market intelligence agent for the "
            "NZ to India honey trade platform. You reason over retrieved "
            "evidence and never fabricate facts. If evidence is missing, "
            "explicitly state 'insufficient evidence'."
        )
