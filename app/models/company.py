import uuid

from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql.base import UUID

from app.models.base import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    mode = Column(String)
    rating = Column(Float)
