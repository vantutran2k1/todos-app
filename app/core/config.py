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
}


class Settings(BaseSettings):
    DATABASE_URL: str = (
        f"postgresql://{_config.get('DB_USER')}:{_config.get('DB_PASSWORD')}@{_config.get('DB_HOST')}:{_config.get('DB_PORT')}/{_config.get('DB_NAME')}"
    )


settings = Settings()
