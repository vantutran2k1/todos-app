from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session

from app.models import Company


class CompanyRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_by_id(self, company_id: UUID) -> Optional[Company]:
        return self._db.query(Company).filter(Company.id == company_id).first()

    def get_by_name(self, name: str) -> Optional[Company]:
        return self._db.query(Company).filter(Company.name == name).first()

    def get_companies(self, page: int, size: int) -> (List[Company], int):
        query = self._db.query(Company)

        total = query.count()
        offset = (page - 1) * size
        companies = query.offset(offset).limit(size).all()

        return companies, total

    def save(self, company: Company):
        self._db.add(company)
        return company
