from fastapi import Query, Depends
from pydantic import BaseModel

from typing import Annotated


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="Номер страницы")]
    per_page: Annotated[int | None, Query(3, ge=1, le=30, description="Количество элементов на странице")]


PaginationDep = Annotated[PaginationParams, Depends()]
