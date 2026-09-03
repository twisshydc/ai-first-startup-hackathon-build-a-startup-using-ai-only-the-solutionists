"""Migrate the NZ honey company master list into the HoneyCompany model.

The existing `nz_honey_master_leads.csv` is treated as the initial seed
dataset for the NZ Honey Company Universe. Each company becomes a
HoneyCompany record with its tier (retained temporarily) mapped to
export_tier and the marketplace status preserved.
"""
import csv
import uuid
from pathlib import Path

from sqlalchemy.orm import Session

from src.db.base import Base
from src.db.session import SessionLocal, engine
from src.models.honey_company import HoneyCompany
from src.services.honey_mapping import TIER_MAP, extract_domain

DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "nz_honey_master_leads.csv"


def seed_honey_companies(db: Session, csv_path: Path = DATA_PATH) -> int:
    if not csv_path.exists():
        raise FileNotFoundError(f"Data file not found: {csv_path}")

    count = 0
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("Company Name", "").strip()
            if not name:
                continue
            existing = db.query(HoneyCompany).filter(HoneyCompany.name == name).first()
            if existing:
                continue

            company = HoneyCompany(
                id=uuid.uuid4(),
                name=name,
                company_type=row.get("Type", "").strip() or None,
                region=row.get("Region/Location", "").strip() or None,
                domain=extract_domain(row.get("Website/Contact", "")),
                marketplace_status=row.get("Marketplace Status", "").strip() or None,
                export_tier=TIER_MAP.get(row.get("Target Tier", "").strip(), None),
            )
            db.add(company)
            count += 1
    db.commit()
    return count


def main() -> int:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        count = seed_honey_companies(db)
        print(f"Seeded {count} honey companies.")
        return count
    finally:
        db.close()


if __name__ == "__main__":
    main()
