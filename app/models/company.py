import uuid
from enum import Enum

from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base


class CompanyMode(str, Enum):
    FREE = "FREE"
    PREMIUM = "PREMIUM"
    ENTERPRISE = "ENTERPRISE"

    @staticmethod
    def from_string(value):
        if value == "FREE":
            return CompanyMode.FREE
        elif value == "PREMIUM":
            return CompanyMode.PREMIUM
        elif value == "ENTERPRISE":
            return CompanyMode.ENTERPRISE
        else:
            raise NotImplementedError(f"Unknown company mode {value}")


class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    mode = Column(String)
    rating = Column(Float)

    users = relationship("User", back_populates="company")
