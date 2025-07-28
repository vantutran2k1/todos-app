from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session

from app.models import Task


class TaskRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_task(self, task_id: UUID) -> Optional[Task]:
        return self._db.query(Task).filter(Task.id == task_id).first()

    def get_tasks_of_user(
        self, user_id: UUID, page: int, size: int
    ) -> (List[Task], int):
        query = self._db.query(Task).where(Task.user_id == user_id)

        total = query.count()
        offset = (page - 1) * size
        tasks = query.offset(offset).limit(size).all()

        return tasks, total

    def save(self, task: Task) -> Task:
        self._db.add(task)
        return task
