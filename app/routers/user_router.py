from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.dependencies.services import get_user_service
from app.schemas.user_schema import CreateUserRequest
from app.services.user_service import UserService

user_router = APIRouter()


@user_router.get("/{user_id}")
def get_user(
    user_id: str,
    include_company: Optional[bool] = Query(default=False),
    user_service: UserService = Depends(get_user_service),
):
    return user_service.get_user(user_id, include_company)


@user_router.get("/")
def get_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, le=100),
    user_service: UserService = Depends(get_user_service),
):
    return user_service.get_users(page, size)


@user_router.post("/")
def create_user(
    request: CreateUserRequest, user_service: UserService = Depends(get_user_service)
):
    return user_service.create_user(request)
