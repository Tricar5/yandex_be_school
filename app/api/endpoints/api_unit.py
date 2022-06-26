from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from starlette.responses import Response, JSONResponse
from fastapi.exceptions import HTTPException

from app.api import deps
from app.crud.crud_unit import CRUDUnit

from app.api.handlers.import_handler import HandlerImport
from app.api.handlers.сhild_handler import HandlerChildren
from app.model.db_models import ShopUnitDB, UnitType
from app.schema.schemas import Error, ShopUnitSchema
from app.schema.request import ShopUnitImportRequest
from app.schema.response import ShopUnitNode
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post(
    "/imports",
    response_model=None,
    status_code=200,
    responses={"400": {"model": Error}},
)
async def post_imports(
        import_obj: ShopUnitImportRequest,
        db: Session = Depends(deps.get_db),
        handler: HandlerImport = Depends(deps.get_import_handler)
) -> Response:

    res = await handler.handle(db, import_obj)

    return Response(status_code=200)



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

    if res is None:
        return JSONResponse(jsonable_encoder(Error(code=404, message="Item not found")), status_code=404)


    return Response(status_code=200)

@router.get(
    "/nodes/{id}",
    response_model=None,
    #responses={"400": {"model": Error}, "404": {"model": Error}},
)
async def get_nodes_id(id: UUID,
                       db: Session = Depends(deps.get_db),
                       handler: HandlerChildren = Depends(deps.get_child_handler),
                       ):

    res = await handler.handle(db, id)

    if res is None:
        return JSONResponse(jsonable_encoder(Error(code=404, message="Item not found", children=None)), status_code=404)

    return jsonable_encoder(res)
