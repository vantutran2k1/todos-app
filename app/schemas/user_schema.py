from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class CreateUserRequest(BaseModel):
    username: str
    password: str = Field(..., min_length=8, max_length=64)
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    company_id: Optional[UUID] = None


class CreateUserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_id: Optional[UUID] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    session_token: str
