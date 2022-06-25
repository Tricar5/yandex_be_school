# generated by fastapi-codegen:
#   filename:  openapi.yaml
#   timestamp: 2022-06-14T16:28:13+00:00


from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class ShopUnitType(Enum):
    OFFER = "OFFER"
    CATEGORY = "CATEGORY"


class ShopImportSchema(BaseModel):
    id: Optional[int] = Field(
        default=None,
    )
    updateDate: datetime = Field(..., description="Время выгрузки")

    class Config:
        orm_mode = True


class ShopUnitSchema(BaseModel):
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
    updateDate: Optional[datetime] = Field(
        None,
        description="Время обновления добавляемых товаров/категорий.",
        example="2022-05-28T21:12:01.000Z",)

    class Config:
        orm_mode = True
        use_enum_values = True


class ShopUnitImportSchema(ShopUnitSchema):
    import_id: int = Field(
        ...,
        description='Номер выгрузки данных',
    )
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
    updateDate: datetime = Field(
        None,
        description="Время добавления товаров/категорий.",
        example="2022-05-28T21:12:01.000Z",
    )

    class Config:
        orm_mode = True
        use_enum_values = True




class Error(BaseModel):
    code: int
    message: str