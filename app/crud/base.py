from typing import Any, Generic, Optional, TypeVar, Union, Type, Dict

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


async def update(
        db: Session,
    *,
    obj: ModelType,
    data: Union[UpdateSchemaType, Dict[str, Any]]
) -> ModelType:
    """
    Функция для обновления полей объекта в БД.
    Передаем объект для изменения в параметр obj.
    Поля для изменения в виде словаря в параметр data
    """

    obj_data = jsonable_encoder(obj)
    if isinstance(data, dict):
        update_data = data
    else:
        update_data = data.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(obj, field, update_data[field])
    db.add(obj)
    return obj


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def init(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        Parameters
        * model: A SQLAlchemy model class
        * schema: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: Session, *args, **kwargs) -> Optional[ModelType]:
        """
        Функция для извлечения объекта из БД.
        Передаем параметры для фильтрации через kwargs.
        """

        statement = select(self.model)
        for attr, value in kwargs.items():
            statement = statement.filter(getattr(self.model, attr) == value)
        statement = await db.execute(statement)
        return statement.scalars().all()

    async def get_first(self, db: Session, *args, **kwargs) -> Optional[ModelType]:
        """
        Функция для извлечения объекта из БД.
        Передаем параметры для фильтрации через kwargs.
        """

        statement = select(self.model)
        for attr, value in kwargs.items():
            statement = statement.filter(getattr(self.model, attr) == value)
        statement = await db.execute(statement)
        return statement.scalars().first()

    async def create(self, db: Session, *, data: CreateSchemaType) -> ModelType:
        """
        Функция для создания объекта в БД.
        Передаем объект для создания в параметр data.
        """
        if isinstance(data, self.model):
            db.add(data)
            return data

        if not isinstance(data, dict):
            obj_data = jsonable_encoder(data)

        db_obj = self.model(**obj_data)
        db.add(db_obj)
        return db_obj

    async def remove(self, db: Session, *args, **kwargs) -> ModelType:
        """
        Функция для удаления объекта из БД.
        Передаем параметры для фильтрации в kwargs.
        """

        statement = delete(self.model)
        for attr, value in kwargs.items():
            statement = statement.filter(getattr(self.model, attr) == value)
        statement = await db.execute(statement)
        await db.commit()
