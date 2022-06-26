from uuid import UUID

from fastapi.encoders import jsonable_encoder
from typing import Dict, Generator, Union
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from app.schema.schemes import ShopUnitImportSchema, ShopImportSchema, ShopUnitSchema
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

        schema_unit_import = [self.generate_unit_imports(import_id, date, item) for item in items]
        db_unit_imports = [ShopUnitImportDB(**schema_unit_import.dict()) for schema_import in schema_unit_import]

        schema_unit = [self.generate_unit(date, item)  for item in items]
        db_units = [ShopUnitDB(**schema_unit.dict()) for item in schema_unit]

        n_exists = []
        exists = []
        for db_unit in db_units:

            # проверяем отсутствие элемента

            not_ex = await self.crud_unit.exists(db, db_unit.id)

            if not_ex:
                n_exists.append(db_unit)

            else:
                exists.append(db_unit)

        if len(n_exists)>0:
            if len(n_exists) == 1:
                res = db.add(n_exists[0])
            else:
                db.add_all(n_exists)

        for db_unit in exists:

            await self.crud_unit.update(db=db, obj=db_unit, data=db_unit.__dict__)

        # Добавляем записи импортов
        res = db.add_all(db_unit_imports)

        return db

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
