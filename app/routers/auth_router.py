from fastapi import APIRouter, Depends, Request, HTTPException, status

from app.dependencies.services import get_auth_service
from app.schemas.user_schema import LoginRequest, LoginResponse
from app.services.auth_service import AuthService

auth_router = APIRouter()


@auth_router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.login(request)


@auth_router.post("/logout")
def logout(request: Request, auth_service: AuthService = Depends(get_auth_service)):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization token missing",
        )
    return auth_service.logout(token)
