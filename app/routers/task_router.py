from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user_id
from app.dependencies.services import get_task_service
from app.schemas.task_schema import CreateTaskRequest
from app.services.task_service import TaskService

task_router = APIRouter()


@task_router.post("/")
def create_task(
    request: CreateTaskRequest,
    current_user: str = Depends(get_current_user_id),
    task_service: TaskService = Depends(get_task_service),
):
    return task_service.create_task(request, current_user)
