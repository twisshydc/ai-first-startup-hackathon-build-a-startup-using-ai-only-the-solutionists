from src.agents import AGENT_REGISTRY, get_agent, get_agent_types


def test_agent_registry_has_all_types():
    expected = {
        "market_research",
        "buyer_discovery",
        "company_intelligence",
        "trade_intelligence",
        "regulatory",
        "competitive_intelligence",
        "revenue",
        "monitoring",
    }
    assert set(get_agent_types()) == expected


def test_get_agent_returns_instance():
    agent = get_agent("revenue")
    assert agent.agent_type == "revenue"


def test_get_agent_unknown_raises():
    try:
        get_agent("does_not_exist")
        assert False, "should have raised"
    except ValueError:
        pass
