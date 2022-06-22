from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.unit_crud import UnitCRUD
from app.schema.schemas import Error, ShopUnitImportRequest

router = APIRouter()


@router.post(
    "/imports",
    response_model=None,
    responses={"400": {"model": Error}},
)
async def post_imports(
    import_obj: ShopUnitImportRequest = None,
    db: Session = Depends(deps.get_db),
    crud: UnitCRUD = Depends(deps.UnitCRUD),
) -> Union[None, Error]:

    async with db.begin():
        res = await crud.create(db, import_obj)  # поколдовать на экземплера

    return


@router.delete(
    "/delete/{id}",
    response_model=None,
    responses={"400": {"model": Error}, "404": {"model": Error}},
)
async def delete_id(id: UUID) -> Union[None, Error]:
    pass
