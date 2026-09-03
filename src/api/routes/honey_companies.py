from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.models.honey_company import HoneyCompany
from src.schemas.honey_company import HoneyCompanyCreate, HoneyCompanyRead

router = APIRouter(prefix="/honey-companies", tags=["honey-companies"])


@router.get("/", response_model=list[HoneyCompanyRead])
def list_honey_companies(db: Session = Depends(get_db)):
    return db.query(HoneyCompany).order_by(HoneyCompany.name).all()


@router.get("/{company_id}", response_model=HoneyCompanyRead)
def get_honey_company(company_id, db: Session = Depends(get_db)):
    company = db.get(HoneyCompany, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.post("/", response_model=HoneyCompanyRead)
def create_honey_company(payload: HoneyCompanyCreate, db: Session = Depends(get_db)):
    company = HoneyCompany(**payload.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company
