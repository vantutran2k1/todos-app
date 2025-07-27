from uuid import uuid4, UUID

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from app.models import Company
from app.models.company import CompanyMode
from app.repositories.company_repository import CompanyRepository
from app.schemas.company_schema import (
    CreateCompanyRequest,
    CreateCompanyResponse,
    GetCompanyResponse,
)
from app.schemas.pagination_meta import PaginationMeta, PaginatedResponse
from app.utils.transactional import transactional


class CompanyService:
    def __init__(self, company_repo: CompanyRepository):
        self._company_repo = company_repo

    def get_company(self, company_id: str):
        company = self._company_repo.get_by_id(UUID(company_id))
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Company not found"
            )

        response = GetCompanyResponse(
            id=company.id,
            name=company.name,
            description=company.description,
            mode=CompanyMode.from_string(company.mode),
            rating=company.rating,
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=response.model_dump(mode="json", exclude_none=True),
        )

    def get_companies(self, page: int, size: int):
        companies, total = self._company_repo.get_companies(page, size)
        data = [
            GetCompanyResponse(
                id=company.id,
                name=company.name,
                description=company.description,
                mode=company.mode,
                rating=company.rating,
            )
            for company in companies
        ]
        meta = PaginationMeta(
            page=page,
            size=size,
            total=total,
            total_pages=(total + size - 1) // size,
        )
        response = PaginatedResponse(data=data, meta=meta).model_dump(
            mode="json", exclude_none=True
        )
        return JSONResponse(status_code=status.HTTP_200_OK, content=response)

    @transactional
    def create_company(self, request: CreateCompanyRequest):
        if self._company_repo.get_by_name(request.name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Company already exists"
            )

        company = Company(
            id=uuid4(),
            name=request.name,
            description=request.description,
            mode=request.mode,
            rating=request.rating,
        )
        saved_company = self._company_repo.save(company)

        response = CreateCompanyResponse(
            id=saved_company.id,
            name=saved_company.name,
            description=saved_company.description,
            mode=saved_company.mode,
            rating=saved_company.rating,
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=response.model_dump(mode="json", exclude_none=True),
        )
