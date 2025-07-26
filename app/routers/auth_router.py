import redis
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db, get_redis_client
from app.schemas.user_schema import LoginRequest, LoginResponse
from app.services.user_service import UserService

auth_router = APIRouter()


@auth_router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis_client),
):
    return UserService(db, redis_client).login(request)
