from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TaskStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class TaskPriority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class BaseTaskResponse(BaseModel):
    id: UUID
    summary: str
    description: Optional[str] = None
    status: str
    priority: str
    user_id: Optional[UUID] = None


class GetTaskResponse(BaseTaskResponse):
    pass


class CreateTaskRequest(BaseModel):
    summary: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.LOW


class CreateTaskResponse(BaseTaskResponse):
    pass


class UpdateTaskStatusRequest(BaseModel):
    status: TaskStatus
