from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.schemas.company_schema import GetCompanyResponse


class BaseUserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class GetUserResponse(BaseUserResponse):
    company: Optional[GetCompanyResponse] = None


class GetUsersResponse(BaseUserResponse):
    company_id: Optional[UUID] = None


class CreateUserRequest(BaseModel):
    username: str
    password: str = Field(..., min_length=8, max_length=64)
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_id: Optional[UUID] = None


class CreateUserResponse(BaseUserResponse):
    company_id: Optional[UUID] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    session_token: str
