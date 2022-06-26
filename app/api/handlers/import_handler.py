from uuid import UUID
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from typing import Dict, Generator, Union, List
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
            #update_date=date
        )

    @classmethod
    def generate_unit(cls, date: datetime, item: ShopUnitImport) -> ShopUnitSchema:
        return ShopUnitSchema(
            id=item.id,
            name=item.name,
            price=item.price,
            type=item.type,
            parentId=item.parentId,
            #update_date=date
        )

    async def handle_import(self, db: AsyncSessionTransaction, date: datetime):
        """
        Получение инкремента для импорта
        :param db: транзакция БД
        :param date: дата
        :return: инкремент
        """
        db_obj = ShopImportDB(update_date=date)

        import_obj = await self.crud_import.create(db, data=db_obj)

        return import_obj

    async def handle_unit_import(self, db, import_id: int, date: datetime,
                                 items: List[ShopUnitImport]):

        """
        Что мы должны сделать:
        Поместить в одну транзакцию новые значения, чтобы избежать конфликта по первичному ключу
        Отключение нарушает целостность таблицы


        :param db: Ассинхронная транзакция
        :param import_id: Инкремент импорта
        :param date: дата
        :param items: объекты - позиции
        :return:
        """
        # создаем схемы данных
        #schema_unit_import = [self.generate_unit_imports(import_id, date, item) for item in items]
        db_unit_imports = []
        for item in items:
            unit_import_item = ShopUnitImportDB(**item.dict())
            unit_import_item.update_date = date
            unit_import_item.import_id = import_id
            db_unit_imports.append(unit_import_item) 

        # создаем модели данных ORM
        schema_unit = [self.generate_unit(date, item) for item in items]
        db_units = []
        for item in items:
            unit_item = ShopUnitDB(**item.dict())
            unit_item.update_date = date
            db_units.append(unit_item) 

        #db_units = [ShopUnitDB(**schema.dict()) for schema in schema_unit]

        for db_unit in db_units:

            # проверяем существует ли такой элемент в базе,
            # если существует достаем его для последующего апдейта
            unit_from_database = await self.crud_unit.get_first(db, id=db_unit.id)
            
            # Если получаем положительное значение, что не существует
            # вставляем в очередь апдейта
            if not unit_from_database:
                await self.crud_unit.create(db=db, data=db_unit)

            else:
                # TODO: реккурсивно обновить всех детей
                # TODO: проверка на изменение категории на оффер
                if unit_from_database.type.value != db_unit.type:
                    continue
                    #raise HTTPException(400, detail="Нельзя изменять категорию!")

                r = await self.crud_unit.update(db=db, obj=unit_from_database, data=db_unit.__dict__)
                    
                # if unit_from_database.children:
                #     list_on_update = unit_from_database.children
                #     while list_on_update:
                #         item = list_on_update.pop()
                #         if item.children:
                #             list_on_update += item.children
                #         r = await self.crud_unit.update(db=db, obj=item, data={
                #             "update_date":db_unit.update_date,
                #             "parentId":item.parentId,
                #             })
                ##
                        



        # Добавляем записи импортов (товарная позиция и импорт)
        res = db.add_all(db_unit_imports)
        await db.commit()

        return res

    async def handle(self, db, data: ShopUnitImportRequest) -> Dict:

        date = data.updateDate
        items = data.items

        # получаем инкремент
        async with db.begin():
            import_model = await self.handle_import(db, date)

            #await db.commit()

        import_id = import_model.id

        # последовательность импорта
        async with db.begin():
            cnt = await self.handle_unit_import(db, import_id, date, items)

        return {'id': import_id, 'date': date, 'total_items': cnt}
