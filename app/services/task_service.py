from uuid import uuid4, UUID

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from app.models import Task
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.schemas.task_schema import CreateTaskRequest, CreateTaskResponse
from app.utils.transactional import transactional


class TaskService:
    def __init__(self, task_repo: TaskRepository, user_repo: UserRepository):
        self._task_repo = task_repo
        self._user_repo = user_repo

    @transactional
    def create_task(self, request: CreateTaskRequest, user_id: UUID):
        if user_id:
            user = self._user_repo.get_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="User not found",
                )

        task = Task(
            id=uuid4(),
            summary=request.summary,
            description=request.description,
            status=request.status.value,
            priority=request.priority.value,
            user_id=user_id,
        )
        saved_task = self._task_repo.save(task)

        response = CreateTaskResponse(
            id=saved_task.id,
            description=saved_task.description,
            status=saved_task.status,
            priority=saved_task.priority,
            user_id=saved_task.user_id,
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=response.model_dump(mode="json", exclude_none=True),
        )
