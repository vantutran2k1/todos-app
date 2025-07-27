from uuid import uuid4

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from app.models.user import User
from app.repositories.company_repository import CompanyRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import (
    CreateUserRequest,
    CreateUserResponse,
)
from app.utils.security import hash_password
from app.utils.transactional import transactional


class UserService:
    def __init__(
        self,
        user_repo: UserRepository,
        company_repo: CompanyRepository,
    ):
        self._user_repo = user_repo
        self._company_repo = company_repo

    @transactional
    def create_user(self, request: CreateUserRequest):
        if self._user_repo.get_by_email(str(request.email)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already in use"
            )

        if self._user_repo.get_by_username(request.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Username already taken"
            )

        if request.company_id:
            company = self._company_repo.get_by_id(request.company_id)
            if not company:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Company not found"
                )

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

        response = CreateUserResponse(
            id=saved_user.id,
            email=saved_user.email,
            username=saved_user.username,
            first_name=saved_user.first_name,
            last_name=saved_user.last_name,
            company_id=saved_user.company_id,
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=response.model_dump(mode="json"),
        )
