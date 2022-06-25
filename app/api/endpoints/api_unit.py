import asyncio
from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, selectinload

from starlette.responses import Response

from app.api import deps
from app.crud.crud_unit import CRUDUnit, CRUDImport

from app.api.handlers.import_handler import HandlerImport

from app.schema.base_schema import Error
from app.schema.request import ShopUnitImportRequest
from app.schema.response import ShopUnitNode

router = APIRouter()


@router.post(
    "/imports",
    response_model=None,
    status_code=201,
    responses={"400": {"model": Error}},
)
async def post_imports(
        import_obj: ShopUnitImportRequest = None,
        db: Session = Depends(deps.get_db),
        handler: HandlerImport = Depends(deps.get_import_handler)
) -> Response:

    res = await handler.handle(db, import_obj)

    return res



@router.delete(
    "/delete/{id}",
    response_model=None,
    responses={"400": {"model": Error}, "404": {"model": Error}},
)
async def delete_id(id: UUID,
                    db: Session = Depends(deps.get_db),
                    crud_unit: CRUDUnit = Depends(deps.get_unit_crud),
                    ) -> Response:

    async with db.begin():
        res = await crud_unit.remove(db, id)

    return Response('', status_code=200)

@router.get(
    "/nodes/{id}",
    #response_model=ShopUnitNode,
    responses={"400": {"model": Error}, "404": {"model": Error}},
)
async def get_nodes_id(id: UUID,
                       db: Session = Depends(deps.get_db),
                       crud_unit: CRUDUnit = Depends(deps.get_unit_crud),
                       ):
    async with db.begin():
        res = await crud_unit.get_first(db, id=id)
    return res
