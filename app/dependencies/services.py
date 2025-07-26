from fastapi import Depends

from app.dependencies.repositories import (
    get_user_repository,
    get_company_repository,
    get_user_session_repository,
)
from app.repositories.company_repository import CompanyRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository
from app.services.auth_service import AuthService
from app.services.company_services import CompanyService
from app.services.user_service import UserService


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
    company_repo: CompanyRepository = Depends(get_company_repository),
) -> UserService:
    return UserService(
        user_repo=user_repo,
        company_repo=company_repo,
    )


def get_company_service(
    company_repo: CompanyRepository = Depends(get_company_repository),
) -> CompanyService:
    return CompanyService(company_repo)


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    user_session_repo: UserSessionRepository = Depends(get_user_session_repository),
) -> AuthService:
    return AuthService(
        user_repo=user_repo,
        user_session_repo=user_session_repo,
    )
