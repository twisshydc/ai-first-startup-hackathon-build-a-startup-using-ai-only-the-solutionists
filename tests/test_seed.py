from src.services.honey_mapping import TIER_MAP, extract_domain


def test_extract_domain_clean():
    assert extract_domain("comvita.co.nz") == "comvita.co.nz"


def test_extract_domain_strips_www():
    assert extract_domain("www.example.com") == "example.com"


def test_extract_domain_rejects_descriptive():
    assert extract_domain("Via Local Stockists") is None
    assert extract_domain("Direct contact / Farm visits") is None
    assert extract_domain("Local Facebook / Community Groups") is None


def test_extract_domain_rejects_contact_prefix():
    assert extract_domain("Contact via Local Directory") is None


def test_tier_map_contains_all_tiers():
    expected = {"Tier 1 (High Priority)", "Tier 2 (Mid Market)", "Tier 3 (Small/Local)", "Tier 4 (Micro/No Marketplace)"}
    assert set(TIER_MAP.keys()) == expected
