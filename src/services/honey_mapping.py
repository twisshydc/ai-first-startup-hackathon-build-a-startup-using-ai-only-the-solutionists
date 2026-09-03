"""Pure helpers for mapping NZ honey lead data into domain records.

Kept separate from the DB session module so they can be imported and tested
without requiring a database driver or connection.
"""

TIER_MAP = {
    "Tier 1 (High Priority)": "tier_1",
    "Tier 2 (Mid Market)": "tier_2",
    "Tier 3 (Small/Local)": "tier_3",
    "Tier 4 (Micro/No Marketplace)": "tier_4",
}


def extract_domain(contact: str) -> str | None:
    contact = contact.strip()
    if not contact or contact.lower().startswith(("via", "local", "contact", "direct")):
        return None
    if " " in contact:
        return None
    return contact.lstrip("www.").lower()
