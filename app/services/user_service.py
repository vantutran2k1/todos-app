from uuid import uuid4, UUID

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from app.models.user import User
from app.repositories.company_repository import CompanyRepository
from app.repositories.user_repository import UserRepository
from app.schemas.company_schema import GetCompanyResponse
from app.schemas.pagination_meta import PaginationMeta, PaginatedResponse
from app.schemas.user_schema import (
    CreateUserRequest,
    CreateUserResponse,
    GetUserResponse,
    GetUsersResponse,
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

    def get_user(self, user_id: str, include_company: bool):
        user = (
            self._user_repo.get_by_id_include_company(UUID(user_id))
            if include_company
            else self._user_repo.get_by_id(UUID(user_id))
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        response = GetUserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        if include_company:
            response.company = GetCompanyResponse(
                id=user.company.id,
                name=user.company.name,
                description=user.company.description,
                mode=user.company.mode,
                rating=user.company.rating,
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=response.model_dump(mode="json", exclude_none=True),
        )

    def get_users(self, page: int, size: int):
        users, total = self._user_repo.get_users(page, size)
        data = [
            GetUsersResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                company_id=user.company_id,
            )
            for user in users
        ]
        meta = PaginationMeta(
            page=page,
            size=size,
            total=total,
            total_pages=(total + size - 1) // size,
        )
        response = PaginatedResponse(data=data, meta=meta).model_dump(
            mode="json", exclude_none=True
        )
        return JSONResponse(status_code=status.HTTP_200_OK, content=response)

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
            content=response.model_dump(mode="json", exclude_none=True),
        )
