from fastapi import Depends
from redis import Redis
from sqlalchemy.orm import Session

from app.db.clients import get_db_session, get_redis_client
from app.repositories.company_repository import CompanyRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository


def get_user_repository(db: Session = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db=db)


def get_company_repository(db: Session = Depends(get_db_session)) -> CompanyRepository:
    return CompanyRepository(db=db)


def get_user_session_repository(
    redis: Redis = Depends(get_redis_client),
) -> UserSessionRepository:
    return UserSessionRepository(redis)
