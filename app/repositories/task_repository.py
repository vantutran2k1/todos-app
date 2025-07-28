from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models import Task


class TaskRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_task(self, task_id: UUID) -> Optional[Task]:
        return self._db.query(Task).filter(Task.id == task_id).first()

    def save(self, task: Task) -> Task:
        self._db.add(task)
        return task
