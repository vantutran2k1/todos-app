from typing import Optional, List
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

    def get_users(self, page: int, size: int) -> (List[User], int):
        query = self._db.query(User)

        total = query.count()
        offset = (page - 1) * size
        users = query.offset(offset).limit(size).all()

        return users, total

    def get_users_of_company(
        self, company_id: UUID, page: int, size: int
    ) -> (List[User], int):
        query = self._db.query(User).where(User.company_id == company_id)

        total = query.count()
        offset = (page - 1) * size
        users = query.offset(offset).limit(size).all()

        return users, total

    def save(self, user: User) -> User:
        self._db.add(user)
        return user
