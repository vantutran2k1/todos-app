from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        return self._db.query(User).filter(User.id == user_id).first()

    def get_by_id_include_company(self, user_id: UUID) -> Optional[User]:
        return (
            self._db.query(User)
            .options(joinedload(User.company))
            .filter(User.id == user_id)
            .first()
        )

    def get_by_email(self, email: str) -> Optional[User]:
        return self._db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        return self._db.query(User).filter(User.username == username).first()

    def save(self, user: User) -> User:
        self._db.add(user)
        return user
