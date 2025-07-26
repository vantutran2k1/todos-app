from redis import Redis

from app.core.settings import settings


class UserSessionRepository:
    def __init__(self, redis_client: Redis):
        self._redis_client = redis_client

    def save_user_session(self, user_id: str, token: str):
        self._redis_client.set(
            f"user_session:{user_id}", token, ex=settings.USER_SESSION_TTL
        )

    def get_user_session(self, user_id: str) -> str:
        return self._redis_client.get(f"user_session:{user_id}")

    def delete_user_session(self, user_id: str):
        self._redis_client.delete(f"user_session:{user_id}")
