from uuid import uuid4, UUID

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from app.models import Task
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.schemas.pagination_meta import PaginationMeta, PaginatedResponse
from app.schemas.task_schema import (
    CreateTaskRequest,
    CreateTaskResponse,
    GetTaskResponse,
)
from app.utils.transactional import transactional


class TaskService:
    def __init__(self, task_repo: TaskRepository, user_repo: UserRepository):
        self._task_repo = task_repo
        self._user_repo = user_repo

    def get_task(self, task_id: str, user_id: str):
        task = self._task_repo.get_task(UUID(task_id))
        if not (task and str(task.user_id) == user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        response = GetTaskResponse(
            id=task.id,
            summary=task.summary,
            description=task.description,
            status=task.status,
            priority=task.priority,
            user_id=task.user_id,
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=response.model_dump(mode="json", exclude_none=True),
        )

    def get_tasks(self, user_id: str, page: int, size: int):
        tasks, total = self._task_repo.get_tasks_of_user(UUID(user_id), page, size)
        data = [
            GetTaskResponse(
                id=task.id,
                summary=task.summary,
                description=task.description,
                status=task.status,
                priority=task.priority,
            ) for task in tasks
        ]
        meta = PaginationMeta(
            page=page,
            size=size,
            total=total,
            total_pages=(total + size - 1) // size,
        )
        response = PaginatedResponse(data=data, meta=meta).model_dump(
            mode="json", exclude_none=True
        )
        return JSONResponse(status_code=status.HTTP_200_OK, content=response)

    @transactional
    def create_task(self, request: CreateTaskRequest, user_id: str):
        if user_id:
            user = self._user_repo.get_by_id(UUID(user_id))
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
            summary=saved_task.summary,
            description=saved_task.description,
            status=saved_task.status,
            priority=saved_task.priority,
            user_id=saved_task.user_id,
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=response.model_dump(mode="json", exclude_none=True),
        )
