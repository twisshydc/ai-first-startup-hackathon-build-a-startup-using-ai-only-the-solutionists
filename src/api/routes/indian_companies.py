from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.models.indian_company import IndianCompany
from src.schemas.indian_company import IndianCompanyCreate, IndianCompanyRead

router = APIRouter(prefix="/indian-companies", tags=["indian-companies"])


@router.get("/", response_model=list[IndianCompanyRead])
def list_indian_companies(db: Session = Depends(get_db)):
    return db.query(IndianCompany).order_by(IndianCompany.name).all()


@router.get("/{company_id}", response_model=IndianCompanyRead)
def get_indian_company(company_id, db: Session = Depends(get_db)):
    company = db.get(IndianCompany, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.post("/", response_model=IndianCompanyRead)
def create_indian_company(payload: IndianCompanyCreate, db: Session = Depends(get_db)):
    company = IndianCompany(**payload.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company
