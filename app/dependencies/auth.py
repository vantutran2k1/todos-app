from uuid import UUID

from fastapi import Header, Depends, HTTPException, status

from app.dependencies.repositories import (
    get_user_session_repository,
    get_user_repository,
)
from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository


def get_current_user_id(
    token: str = Header(..., alias="Authorization"),
    user_session_repo: UserSessionRepository = Depends(get_user_session_repository),
) -> str:
    user_id = user_session_repo.get_user_session(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return user_id


def get_current_admin_user_id(
    user_id: str = Depends(get_current_user_id),
    user_repo: UserRepository = Depends(get_user_repository),
) -> str:
    user = user_repo.get_by_id(UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient privileges",
        )

    return user_id
