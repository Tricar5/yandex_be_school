from uuid import UUID

from app.crud.base import CRUDBase
from app.model.db_models import ShopUnitDB, ShopImportDB, ShopUnitImportDB

from app.schema.schemas import ShopImportSchema, ShopUnitSchema, ShopUnitImportSchema

from sqlalchemy.ext.asyncio import AsyncSession as Session
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, delete, func

class CRUDUnit(CRUDBase[ShopUnitDB, ShopUnitSchema, ShopUnitSchema]):
    """
    Унаследованный CRUD класс для операций с выгрузками
    """
    async def exists(self, db: Session, value) -> int:
        """
        Функция для извлечения объекта из БД.
        Передаем параметры для фильтрации через kwargs.
        """

        statement = select(self.model)
        statement = statement.filter(self.model.id == value)
        statement = await db.execute(statement)
        el = statement.scalars().all()
        return len(el) == 0

    async def non_exists_newer(self, db: Session, date) -> int:
        """
        Функция для извлечения объекта из БД.
        Передаем параметры для фильтрации через kwargs.
        """

        statement = select(self.model)
        statement = statement.filter(self.model.updateDate >= date)
        statement = await db.execute(statement)
        el = statement.scalars().all()
        return len(el) == 0

    def recalculate_avg_prices(self, db: Session) -> int:
        """
        Функция рекалькуляции средних значений для категорий
        """
        pass
        #statement = select(self.model.c.parentId,func.max(self.model.c.parentId)).filter(self.model.type == 'OFFER').groupby(self.model.c.parentId)
        #statement = await db.execute(statement)
        #el = statement.scalars().all()
        #return len(el) == 0

    async def remove(self, db: Session, unit_id: UUID) -> UUID:
        """
        Функция для удаления объекта из БД по id
        """
        stmt = select(self.model).filter(self.model.id == unit_id)
        stmt = await db.execute(stmt)
        obj = stmt.scalars().all()

        # если запрос пустой, то удаление не требуется и возвращаем, что объект не найден
        if len(obj) == 0:
            return None

        stmt = select(self.model).filter(getattr(self.model, "id") == unit_id)
        res = await db.execute(stmt)

        if len(res) == 0:
            return 0

        statement = delete(self.model)
        statement = statement.filter(getattr(self.model, "id") == unit_id)
        statement = await db.execute(statement)
        #await db.commit()

        return unit_id


class CRUDUnitImport(CRUDBase[ShopUnitImportDB, ShopUnitImportSchema, ShopUnitImportSchema]):
    ...


class CRUDImport(CRUDBase[ShopImportDB, ShopImportSchema, ShopImportSchema]):

    async def create(self, db: Session, *, data: ShopImportSchema) -> ShopImportSchema:
        """
        Функция для создания объекта в БД.
        Передаем объект для создания в параметр data.
        """

        if isinstance(data, self.model):
            db.add(data)
            return data

        if not isinstance(data, dict):
            obj_data = jsonable_encoder(data)

        db_obj: ShopImportDB = self.model(**obj_data)
        db.add(db_obj)

        return db_obj
