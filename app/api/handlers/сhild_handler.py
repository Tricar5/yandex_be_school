from uuid import UUID

from fastapi.encoders import jsonable_encoder
from typing import Dict, Generator, Union
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from app.schema.schemes import ShopUnitImportSchema, ShopImportSchema, ShopUnitSchema
from app.schema.request import ShopUnitImport, ShopUnitImportRequest
from app.schema.response import ShopUnitNode
from app.model.db_models import ShopImportDB, ShopUnitDB, ShopUnitImportDB
from app.crud.crud_unit import CRUDUnitImport, CRUDImport, CRUDUnit


# from sqlalchemy import exists, select


class HandlerChildren:
    def __init__(self, crud_unit: CRUDUnit):
        self.crud_unit = crud_unit


    async def handle(self, db, unit_id: UUID) -> ShopUnitNode:
        async with db.begin():
            res = await self.crud_unit.get_first(db, id=unit_id)

        #if len(res) == 0:
        #    return None

        return res
