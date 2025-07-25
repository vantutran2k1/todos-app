from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Company
from app.repositories.company_repository import CompanyRepository
from app.schemas.company_schema import CreateCompanyRequest, CreateCompanyResponse


class CompanyService:
    def __init__(self, db: Session):
        self._company_repo = CompanyRepository(db)

    def create_company(self, request: CreateCompanyRequest) -> CreateCompanyResponse:
        if self._company_repo.get_by_name(request.name):
            raise HTTPException(status_code=409, detail="Company already exists")

        company = Company(
            id=uuid4(),
            name=request.name,
            description=request.description,
            mode=request.mode,
            rating=request.rating,
        )
        saved_company = self._company_repo.save(company)

        return CreateCompanyResponse(
            company_id=saved_company.id,
            name=saved_company.name,
            description=saved_company.description,
            mode=saved_company.mode,
            rating=saved_company.rating,
        )
