from typing import Union
from uuid import UUID


from fastapi import APIRouter, Depends
from starlette.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, selectinload


from app.api import deps
from app.crud.crud_unit import CRUDUnit
from app.api.handlers.import_handler import handle_import
from sqlalchemy.ext.asyncio import AsyncEngine

from app.schema.schemas import Error, ShopUnitImportRequest, ValidationError



router = APIRouter()

@router.post(
    "/imports",
    response_model=None,
    status_code=201,
    description='Вставка или обновление прошли успешно.',
    responses={"400": {"model": Error},},
)
async def post_imports(
    import_obj: ShopUnitImportRequest,
    async_eng: AsyncEngine = Depends(deps.get_eng),
    crud_unit: CRUDUnit = Depends(deps.get_import_crud),
) -> Union[Error, Response]:
    res = await crud_unit.import_create(async_eng, import_obj)
    return Response('Вставка или обновление прошли успешно.', status_code=201)


@router.delete(
    "/delete/{id}",
    response_model=None,
    responses={"400": {"model": Error}, "404": {"model": Error}},
)
async def delete_id(id: UUID,
                    async_eng: AsyncEngine = Depends(deps.get_eng),
                    crud_unit: CRUDUnit = Depends(deps.get_import_crud),
                    ) -> Union[None, Error]:

    res = await crud_unit.delete_unit(async_eng, id)
    return Response
