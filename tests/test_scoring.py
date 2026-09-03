from src.services.scoring import BuyerScorer, NZCompanyScorer, ScoreComponent, ScoreResult


class FakeCompany:
    def __init__(self, **attrs):
        self.__dict__.update(attrs)


def test_nz_scorer_perfect_company():
    company = FakeCompany(
        product_market_fit=1.0,
        premium_positioning=1.0,
        export_readiness=1.0,
        production_scale=1.0,
        manuka_exposure=1.0,
        operational_readiness=1.0,
        evidence_quality=1.0,
    )
    result = NZCompanyScorer().score(company)
    assert result.total == 100.0


def test_nz_scorer_zero_company():
    company = FakeCompany()
    result = NZCompanyScorer().score(company)
    assert result.total == 0.0


def test_nz_scorer_partial():
    company = FakeCompany(product_market_fit=1.0, manuka_exposure=1.0)
    result = NZCompanyScorer().score(company)
    assert 0 < result.total < 100


def test_nz_scorer_weights_sum_to_100():
    scorer = NZCompanyScorer()
    assert sum(scorer.WEIGHTS.values()) == 100


def test_buyer_scorer_total():
    company = FakeCompany(
        relevance_score=1.0,
        product_fit=1.0,
        purchasing_capability=1.0,
        distribution_footprint=1.0,
        premium_compatibility=1.0,
        evidence_quality=1.0,
    )
    result = BuyerScorer().score(company)
    assert result.total == 100.0


def test_score_result_explains():
    company = FakeCompany(product_market_fit=1.0)
    result = NZCompanyScorer().score(company, evidence=["source: comvita.co.nz"])
    explanation = result.explain()
    assert "Total:" in explanation
    assert "product_market_fit" in explanation
