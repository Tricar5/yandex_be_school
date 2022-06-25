from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, validator, ValidationError


from app.schema.base_schema import ShopUnitType
from app.schema.base_schema import Error


class ShopUnitImport(BaseModel):
    id: UUID = Field(
        ...,
        description="Уникальный идентификатор",
        example="3fa85f64-5717-4562-b3fc-2c963f66a333",
    )
    name: str = Field(..., description="Имя элемента.")
    parentId: Optional[UUID] = Field(
        default=None,
        description="UUID родительской категории",
        example="3fa85f64-5717-4562-b3fc-2c963f66a333",
    )
    type: ShopUnitType
    price: Optional[int] = Field(
        default=None,
        description="Целое число, для категорий поле должно содержать null.",
    )


class ShopUnitImportRequest(BaseModel):
    items: Optional[List[ShopUnitImport]] = Field(
        None, description="Импортируемые элементы"
    )
    updateDate: str = Field(
        None,
        description="Время обновления добавляемых товаров/категорий.",
        example="2022-05-28T21:12:01.000Z",
    )

    @validator('updateDate')
    def validate_dt(cls, v):
        if not datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f%z'):
            raise Error(code=400, message='Невалидная схема документа или входные данные не верны.')
        return datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f%z')
