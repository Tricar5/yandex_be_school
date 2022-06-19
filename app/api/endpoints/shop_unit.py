from fastapi import APIRouter, FastAPI

from typing import Union
from uuid import UUID

from app.schemas.schemas import (
    ShopUnitImportRequest,
    Error
    )

router = APIRouter()



@router.post('/imports', response_model=None, responses={'400': {'model': Error}})
def post_imports(body: ShopUnitImportRequest = None) -> Union[None, Error]:
    pass


@router.delete(
    '/delete/{id}',
    response_model=None,
    responses={'400': {'model': Error}, '404': {'model': Error}},
)
def delete_delete_id(id: UUID) -> Union[None, Error]:
    pass
