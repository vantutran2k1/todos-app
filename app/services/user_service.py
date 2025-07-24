from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import CreateUserRequest, CreateUserResponse
from app.utils.security import hash_password


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create_user(self, request: CreateUserRequest) -> CreateUserResponse:
        if self.repo.get_by_email(str(request.email)):
            raise HTTPException(status_code=409, detail="Email already in use")

        if self.repo.get_by_username(request.username):
            raise HTTPException(status_code=409, detail="Username already taken")

        user = User(
            id=uuid4(),
            email=str(request.email),
            username=request.username,
            first_name=request.first_name,
            last_name=request.last_name,
            hashed_password=hash_password(request.password),
            is_active=True,
            is_admin=False,
        )
        saved_user = self.repo.save(user)

        return CreateUserResponse(
            id=saved_user.id,
            email=saved_user.email,
            username=saved_user.username,
            first_name=saved_user.first_name,
            last_name=saved_user.last_name,
        )
