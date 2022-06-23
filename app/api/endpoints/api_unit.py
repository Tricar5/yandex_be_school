from typing import Union
from uuid import UUID


from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, selectinload

from starlette.responses import Response

from app.api import deps
from app.crud.crud_unit import UnitCRUD, ImportCRUD



from app.api.handlers.import_handler import handle_import


from app.schema.schemas import Error, ShopUnitImportRequest



router = APIRouter()




@router.post(
    "/imports",
    response_model=None,
    status_code = 201,
    responses={"400": {"model": Error}},
)
async def post_imports(
    import_obj: ShopUnitImportRequest = None,
    db: Session = Depends(deps.get_db),
    c_unit: UnitCRUD = Depends(deps.get_unit_crud),
    c_import: ImportCRUD = Depends(deps.get_import_crud),
) -> Union[None, Error]:



    async with db.begin():
        res = await handle_import(db, c_unit, c_import, data=import_obj)

    return {'res': res}


@router.delete(
    "/delete/{id}",
    response_model=None,
    responses={"400": {"model": Error}, "404": {"model": Error}},
)
async def delete_id(id: UUID) -> Union[None, Error]:
    pass
