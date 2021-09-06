from typing import Callable, Type

from app.crud.base import CrudBase
from databases import Database
from fastapi import Depends
from starlette.requests import Request


def get_database(request: Request) -> Database:
    return request.app.state._db


def get_crud(crudType: Type[CrudBase]) -> Callable:
    def get_crud_type(db: Database = Depends(get_database)) -> Type[CrudBase]:
        return crudType(db)

    return get_crud_type
