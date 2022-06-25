from uuid import UUID

from fastapi.encoders import jsonable_encoder
from typing import Dict, Generator, Union
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from app.schema.base_schema import ShopUnitImportSchema, ShopImportSchema, ShopUnitSchema
from app.schema.request import ShopUnitImport, ShopUnitImportRequest
from app.model.db_models import ShopImportDB, ShopUnitDB, ShopUnitImportDB
from app.crud.crud_unit import CRUDUnitImport, CRUDImport, CRUDUnit


# from sqlalchemy import exists, select


class HandlerImport:
    def __init__(self, crud_import: CRUDImport, crud_u_import: CRUDUnitImport, crud_unit: CRUDUnit):
        self.crud_import = crud_import
        self.crud_u_import = crud_u_import
        self.crud_unit = crud_unit

    @classmethod
    def generate_unit_imports(cls, import_id: int, date: datetime, item: ShopUnitImport) -> ShopUnitImportSchema:
        return ShopUnitImportSchema(
            import_id=import_id,
            id=item.id,
            name=item.name,
            price=item.price,
            type=item.type,
            parentId=item.parentId,
            updateDate=date
        )

    @classmethod
    def generate_unit(cls, date: datetime, item: ShopUnitImport) -> ShopUnitSchema:
        return ShopUnitSchema(
            id=item.id,
            name=item.name,
            price=item.price,
            type=item.type,
            parentId=item.parentId,
            updateDate=date
        )

    async def handle_import(self, db: AsyncSessionTransaction, date: datetime):

        db_obj = ShopImportDB(updateDate=date)

        import_obj = await self.crud_import.create(db, data=db_obj)

        return import_obj

    async def handle_unit_import(self, db, import_id: int, date: datetime,
                                 items: ShopUnitImport):
        cnt = 0
        for item in items:
            schema_unit = self.generate_unit(date, item)
            schema_unit_import = self.generate_unit_imports(import_id, date, item)

            db_unit = ShopUnitDB(**schema_unit.dict())

            db_unit_import = ShopUnitImportDB(**schema_unit_import.dict())

            # проверяем отсутствие элемента

            res = await self.crud_unit.exists(db, db_unit.id)

            if res:
                db_unit = await self.crud_unit.create(db=db, data=db_unit)

            else: # элемент существует
                # проверяем отсутствие элемента с большей датой обновления
                newer = await self.crud_unit.exists_newer(db, db_unit.updateDate)
                if newer:
                    db_unit = await self.crud_unit.update(db=db, obj=db_unit, data=schema_unit)

            # Добавляем записи импортов
            db_unit_import = await self.crud_u_import.create(db=db, data=db_unit_import)
            cnt += 1

        return cnt

    async def handle(self, db, data: ShopUnitImportRequest) -> Dict:

        date = data.updateDate
        items = data.items

        async with db.begin():
            import_model = await self.handle_import(db, date)

            await db.commit()

        import_id = import_model.id

        async with db.begin():
            cnt = await self.handle_unit_import(db, import_id, date, items)

        return {'id': import_id, 'date': date, 'total_items': cnt}
