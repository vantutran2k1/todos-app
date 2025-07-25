from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app import schemas
from app.db.session import get_db
from app.schemas.company_schema import CreateCompanyRequest, CreateCompanyResponse
from app.services.company_services import CompanyService

company_router = APIRouter()


@company_router.post("/", response_model=CreateCompanyResponse)
def create_company(request: CreateCompanyRequest, db: Session = Depends(get_db)):
    return CompanyService(db).create_company(request)
