from uuid import uuid4

from fastapi import HTTPException

from app.models.user import User
from app.repositories.company_repository import CompanyRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository
from app.schemas.user_schema import (
    CreateUserRequest,
    CreateUserResponse,
    LoginRequest,
    LoginResponse,
)
from app.utils.security import hash_password, verify_password, generate_session_token


class UserService:
    def __init__(
        self,
        user_repo: UserRepository,
        company_repo: CompanyRepository,
        user_session_repo: UserSessionRepository,
    ):
        self._user_repo = user_repo
        self._company_repo = company_repo
        self._user_session_repo = user_session_repo

    def create_user(self, request: CreateUserRequest) -> CreateUserResponse:
        if self._user_repo.get_by_email(str(request.email)):
            raise HTTPException(status_code=409, detail="Email already in use")

        if self._user_repo.get_by_username(request.username):
            raise HTTPException(status_code=409, detail="Username already taken")

        if request.company_id:
            company = self._company_repo.get_by_id(request.company_id)
            if not company:
                raise HTTPException(status_code=404, detail="Company not found")

        user = User(
            id=uuid4(),
            email=str(request.email),
            username=request.username,
            first_name=request.first_name,
            last_name=request.last_name,
            hashed_password=hash_password(request.password),
            is_active=True,
            is_admin=False,
            company_id=request.company_id,
        )
        saved_user = self._user_repo.save(user)

        return CreateUserResponse(
            id=saved_user.id,
            email=saved_user.email,
            username=saved_user.username,
            first_name=saved_user.first_name,
            last_name=saved_user.last_name,
            company_id=saved_user.company_id,
        )

    def login(self, request: LoginRequest) -> LoginResponse:
        user = self._user_repo.get_by_username(request.username)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid username or password")
        if not verify_password(request.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid username or password")

        token = generate_session_token()
        self._user_session_repo.save_user_session(user.id, token)
        return LoginResponse(session_token=token)
