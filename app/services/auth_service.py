from alembic.util import status
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository
from app.schemas.user_schema import LoginRequest, LoginResponse
from app.utils.security import verify_password, generate_session_token


class AuthService:
    def __init__(
        self, user_repo: UserRepository, user_session_repo: UserSessionRepository
    ):
        self._user_repo = user_repo
        self._user_session_repo = user_session_repo

    def login(self, request: LoginRequest) -> LoginResponse:
        user = self._user_repo.get_by_username(request.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid username or password",
            )
        if not verify_password(request.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid username or password",
            )

        session_token = generate_session_token()
        self._user_session_repo.save_user_session(user.id, session_token)
        return LoginResponse(session_token=session_token)

    def logout(self, token: str):
        result = self._user_session_repo.delete_user_session(token)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Successfully logged out"},
        )
