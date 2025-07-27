from fastapi import APIRouter, Depends, Query

from app.dependencies.auth import get_current_admin_user_id
from app.dependencies.services import get_company_service
from app.schemas.company_schema import CreateCompanyRequest
from app.services.company_service import CompanyService

company_router = APIRouter()


@company_router.get("/{company_id}")
def get_company(
    company_id: str, company_service: CompanyService = Depends(get_company_service)
):
    return company_service.get_company(company_id)


@company_router.get("/")
def get_companies(
    page: int = Query(1, ge=1),
    size: int = Query(10, le=100),
    company_service: CompanyService = Depends(get_company_service),
):
    return company_service.get_companies(page, size)


@company_router.post("/")
def create_company(
    request: CreateCompanyRequest,
    user_id: str = Depends(get_current_admin_user_id),
    company_service: CompanyService = Depends(get_company_service),
):
    return company_service.create_company(request)
