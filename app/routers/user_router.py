from fastapi import APIRouter, Depends

from app.dependencies.services import get_user_service
from app.schemas.user_schema import CreateUserRequest, CreateUserResponse
from app.services.user_service import UserService

user_router = APIRouter()


@user_router.post("/", response_model=CreateUserResponse)
def create_user(
    request: CreateUserRequest, user_service: UserService = Depends(get_user_service)
):
    return user_service.create_user(request)
