from typing import Generic, TypeVar, List

from pydantic import BaseModel


class PaginationMeta(BaseModel):
    page: int
    size: int
    total: int
    total_pages: int


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    meta: PaginationMeta

    class Config:
        arbitrary_types_allowed = True
