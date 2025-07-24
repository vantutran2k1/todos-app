from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user_schema import CreateUserRequest, CreateUserResponse
from app.services.user_service import UserService

user_router = APIRouter()


@user_router.post("/", response_model=CreateUserResponse)
def create_user(request: CreateUserRequest, db: Session = Depends(get_db)):
    return UserService(db).create_user(request)
