from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models import Company


class CompanyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, company_id: UUID) -> Optional[Company]:
        return self.db.query(Company).filter(Company.id == company_id).first()

    def get_by_name(self, name: str) -> Optional[Company]:
        return self.db.query(Company).filter(Company.name == name).first()

    def save(self, company: Company):
        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)
        return company
