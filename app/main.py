from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST

from app.routers.auth_router import auth_router
from app.routers.company_router import company_router
from app.routers.task_router import task_router
from app.routers.user_router import user_router

app = FastAPI(title="Todos App", version="1.0.0")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={
            "detail": jsonable_encoder(exc.errors()),
            "body": exc.body,
        },
    )


app.include_router(router=auth_router, tags=["auth"], prefix="/api/v1/auth")
app.include_router(router=user_router, tags=["users"], prefix="/api/v1/users")
app.include_router(
    router=company_router, tags=["companies"], prefix="/api/v1/companies"
)
app.include_router(router=task_router, tags=["tasks"], prefix="/api/v1/tasks")
