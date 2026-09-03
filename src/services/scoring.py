from dataclasses import dataclass, field


@dataclass
class ScoreComponent:
    """An individual scoring dimension.

    `score` is the raw dimension score on a 0-100 scale.
    `weighted` is the contribution to the total = score * weight.
    """
    name: str
    score: float      # 0-100 raw
    weight: float     # percentage weight (weights sum to 100)
    max_score: float  # target (weight-based) for this dimension
    evidence: list[str] = field(default_factory=list)

    @property
    def weighted(self) -> float:
        return self.score * (self.weight / 100.0)


@dataclass
class ScoreResult:
    """Explainable scoring result for a company."""
    total: float
    components: list[ScoreComponent]

    def explain(self) -> str:
        lines = [f"Total: {self.total:.1f}/100", ""]
        for comp in self.components:
            lines.append(
                f"{comp.name}: {comp.score:.0f}/100 "
                f"(weight {comp.weight:.0f}%, max contribution {comp.weight:.1f}) "
                f"→ {comp.weighted:.1f}"
            )
            if comp.evidence:
                lines.append("  Evidence:")
                for e in comp.evidence:
                    lines.append(f"    • {e}")
        return "\n".join(lines)


class NZCompanyScorer:
    """Scores NZ honey companies for India market expansion fit.

    Dimensions (configurable):
    - product-market fit
    - premium positioning
    - export readiness
    - production scale
    - manuka exposure
    - operational readiness
    - evidence quality
    """

    WEIGHTS = {
        "product_market_fit": 20,
        "premium_positioning": 15,
        "export_readiness": 20,
        "production_scale": 15,
        "manuka_exposure": 15,
        "operational_readiness": 10,
        "evidence_quality": 5,
    }

    def score(self, company, evidence: list[str] | None = None) -> ScoreResult:
        evidence = evidence or []
        components = []
        for name, weight in self.WEIGHTS.items():
            value = getattr(company, name, None)
            raw = self._normalise(value)
            score = raw * 100
            components.append(
                ScoreComponent(
                    name=name,
                    score=score,
                    weight=weight,
                    max_score=weight,
                    evidence=evidence,
                )
            )
        total = min(sum(c.weighted for c in components), 100.0)
        return ScoreResult(total=total, components=components)

    @staticmethod
    def _normalise(value) -> float:
        """Return a 0-1 normalised value. None -> 0."""
        if value is None:
            return 0.0
        if value < 0 or value > 1:
            value = value / 100.0
        return value


class BuyerScorer:
    """Scores Indian companies as potential buyers.

    Dimensions:
    - relevance
    - product fit
    - purchasing capability
    - distribution footprint
    - premium compatibility
    - evidence quality
    """

    WEIGHTS = {
        "relevance_score": 20,
        "product_fit": 20,
        "purchasing_capability": 15,
        "distribution_footprint": 15,
        "premium_compatibility": 15,
        "evidence_quality": 15,
    }

    def score(self, company, evidence: list[str] | None = None) -> ScoreResult:
        evidence = evidence or []
        components = []
        for name, weight in self.WEIGHTS.items():
            value = getattr(company, name, None)
            raw = self._normalise(value)
            score = raw * 100
            components.append(
                ScoreComponent(
                    name=name,
                    score=score,
                    weight=weight,
                    max_score=weight,
                    evidence=evidence,
                )
            )
        total = min(sum(c.weighted for c in components), 100.0)
        return ScoreResult(total=total, components=components)

    @staticmethod
    def _normalise(value) -> float:
        if value is None:
            return 0.0
        if value < 0 or value > 1:
            value = value / 100.0
        return value
