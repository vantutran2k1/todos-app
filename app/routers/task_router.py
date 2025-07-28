from fastapi import APIRouter, Depends, Query

from app.dependencies.auth import get_current_user_id
from app.dependencies.services import get_task_service
from app.schemas.task_schema import CreateTaskRequest
from app.services.task_service import TaskService

task_router = APIRouter()


@task_router.get("/{task_id}")
def get_task(
    task_id: str,
    current_user: str = Depends(get_current_user_id),
    task_service: TaskService = Depends(get_task_service),
):
    return task_service.get_task(task_id, current_user)


@task_router.get("/")
def get_tasks(
    page: int = Query(1, ge=1),
    size: int = Query(10, le=100),
    current_user: str = Depends(get_current_user_id),
    task_service: TaskService = Depends(get_task_service),
):
    return task_service.get_tasks(current_user, page, size)


@task_router.post("/")
def create_task(
    request: CreateTaskRequest,
    current_user: str = Depends(get_current_user_id),
    task_service: TaskService = Depends(get_task_service),
):
    return task_service.create_task(request, current_user)
