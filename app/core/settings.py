import os
from typing import Dict, Any

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

_config: Dict[str, Any] = {
    "DB_HOST": os.getenv("DB_HOST", "localhost"),
    "DB_PORT": os.getenv("DB_PORT", "5432"),
    "DB_USER": os.getenv("DB_USER", ""),
    "DB_PASSWORD": os.getenv("DB_PASSWORD", ""),
    "DB_NAME": os.getenv("DB_NAME", ""),
    "REDIS_HOST": os.getenv("REDIS_HOST", "localhost"),
    "REDIS_PORT": os.getenv("REDIS_PORT", "6379"),
    "REDIS_DB": os.getenv("REDIS_DB", "0"),
    "USER_SESSION_TTL": os.getenv("USER_SESSION_TTL", "3600"),
}


class Settings(BaseSettings):
    DATABASE_URL: str = (
        f"postgresql://{_config.get('DB_USER')}:{_config.get('DB_PASSWORD')}@{_config.get('DB_HOST')}:{_config.get('DB_PORT')}/{_config.get('DB_NAME')}"
    )
    REDIS_HOST: str = _config.get("REDIS_HOST")
    REDIS_PORT: int = int(_config.get("REDIS_PORT"))
    REDIS_DB: int = int(_config.get("REDIS_DB"))
    USER_SESSION_TTL: int = int(_config.get("USER_SESSION_TTL"))


settings = Settings()
