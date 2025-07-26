from fastapi import APIRouter, Depends

from app.dependencies.services import get_company_service
from app.schemas.company_schema import CreateCompanyRequest, CreateCompanyResponse
from app.services.company_services import CompanyService

company_router = APIRouter()


@company_router.post("/", response_model=CreateCompanyResponse)
def create_company(
    request: CreateCompanyRequest,
    company_service: CompanyService = Depends(get_company_service),
):
    return company_service.create_company(request)
