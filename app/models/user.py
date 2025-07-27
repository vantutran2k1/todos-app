import uuid

from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    company_id = Column(
        UUID(as_uuid=True), ForeignKey("companies.id", ondelete="SET NULL")
    )
    company = relationship("Company", back_populates="users")
