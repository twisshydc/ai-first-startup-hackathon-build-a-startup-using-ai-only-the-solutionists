from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import honey_companies, indian_companies, research

app = FastAPI(
    title="Solutionists — NZ → India Honey Trade Intelligence Platform",
    version="0.1.0",
    description=(
        "Trade intelligence and operations platform for New Zealand honey "
        "companies entering the Indian market."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(honey_companies.router)
app.include_router(indian_companies.router)
app.include_router(research.router)


@app.get("/")
def root():
    return {
        "service": "solutionsists",
        "version": "0.1.0",
        "status": "ok",
        "focus": "NZ honey → India trade intelligence",
    }
