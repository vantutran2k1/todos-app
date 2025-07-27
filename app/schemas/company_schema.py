from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.company import CompanyMode


class BaseCompanyResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    mode: CompanyMode
    rating: Optional[float] = None


class GetCompanyResponse(BaseCompanyResponse):
    pass


class CreateCompanyRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=256)
    description: Optional[str] = None
    mode: Optional[CompanyMode] = CompanyMode.FREE
    rating: Optional[float] = Field(None, ge=0, le=5)


class CreateCompanyResponse(BaseCompanyResponse):
    pass
