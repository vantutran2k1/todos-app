from typing import Generator

import redis
from redis.client import Redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.settings import settings

# --- SQLAlchemy ---
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=True if settings.ENV == "dev" else False,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> Generator[Session, None, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Redis ---
_redis_client: Redis = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)


def get_redis_client() -> Redis:
    return _redis_client
