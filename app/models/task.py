import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql.base import UUID

from app.models.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    summary = Column(String)
    description = Column(String)
    status = Column(String)
    priority = Column(String)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
