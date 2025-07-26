from fastapi import APIRouter, Depends

from app.dependencies.services import get_user_service
from app.schemas.user_schema import LoginRequest, LoginResponse
from app.services.user_service import UserService

auth_router = APIRouter()


@auth_router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, user_service: UserService = Depends(get_user_service)):
    return user_service.login(request)
