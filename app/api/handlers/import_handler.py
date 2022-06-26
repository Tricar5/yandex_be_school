from uuid import UUID

from fastapi.encoders import jsonable_encoder
from typing import Dict, Generator, Union
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from app.schema.schemas import ShopUnitImportSchema, ShopImportSchema, ShopUnitSchema
from app.schema.request import ShopUnitImport, ShopUnitImportRequest
from app.model.db_models import ShopImportDB, ShopUnitDB, ShopUnitImportDB
from app.crud.crud_unit import CRUDUnitImport, CRUDImport, CRUDUnit


# from sqlalchemy import exists, select


class HandlerImport:
    """
    Класс обеспечивающий импорт и вставку новых значений
    """
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

        """
        Что мы должны сделать:
        Поместить в одну транзакцию новые значения, чтобы избежать конфликта по первичному ключу
        Отключение нарушает целостность таблицы


        :param db:
        :param import_id:
        :param date:
        :param items:
        :return:
        """
        # создаем схемы данных
        schema_unit_import = [self.generate_unit_imports(import_id, date, item) for item in items]
        db_unit_imports = [ShopUnitImportDB(**schema.dict()) for schema in schema_unit_import]

        # создаем модели данных ORM
        schema_unit = [self.generate_unit(date, item) for item in items]
        db_units = [ShopUnitDB(**schema.dict()) for schema in schema_unit]

        # массив выгрузки
        n_exists = []
        exists = []

        for db_unit in db_units:

            # проверяем отсутствие элемента

            not_ex = await self.crud_unit.exists(db, db_unit.id)
            # Если получаем положительное значение, что не существует
            # вставляем в очередь апдейта
            if not_ex:
                n_exists.append(db_unit)

            else:
                exists.append(db_unit)

        # Вставляем недостающие данных
        if len(n_exists) > 0:
            if len(n_exists) == 1:
                res = db.add(n_exists[0])
            else:
                db.add_all(n_exists)

        # Делаем апдейты...
        for i in range(len(exists)):

            exists[i] = await self.crud_unit.update(db=db, obj=exists[i], data=exists[i].__dict__)

        # Добавляем записи импортов (товарная позиция и импорт)
        res = db.add_all(db_unit_imports)

        return res

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
