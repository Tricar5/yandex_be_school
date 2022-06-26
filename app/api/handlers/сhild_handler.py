from uuid import UUID

from fastapi.encoders import jsonable_encoder
from typing import Dict, Generator, Union
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from app.schema.schemas import ShopUnitImportSchema, ShopImportSchema, ShopUnitSchema
from app.schema.request import ShopUnitImport, ShopUnitImportRequest
from app.schema.response import ShopUnitNode
from app.model.db_models import ShopImportDB, ShopUnitDB, ShopUnitImportDB, UnitType
from app.crud.crud_unit import CRUDUnitImport, CRUDImport, CRUDUnit


# from sqlalchemy import exists, select
def comp_mean(array):
    length = len(array)
    return sum(array)/length

class HandlerChildren:
    def __init__(self, crud_unit: CRUDUnit):
        self.crud_unit = crud_unit
    async def traverse_response_tree(self, basic_tree: ShopUnitDB):

        """
        Трассировка и форматирования nested дерева из базы
        :param d: Результ lazyloading с помощью ORM модели
        :return:
        """
        def recursive(node: ShopUnitDB):
            if node.type == UnitType.CATEGORY:
                return {
                "id": node.id,
                "name": node.name,
                "parentId": node.parentId,
                "price": comp_mean([child.price for child in node.children]),
                "date": node.update_date,
                "type": node.type,
                "children": [recursive(child) for child in node.children]
                }
            else:
                return {
                "id": node.id,
                "name": node.name,
                "parentId": node.parentId,
                "price": node.price,
                "date": node.update_date,
                "type": node.type,
                "children": None
                }

        return recursive(basic_tree)


    async def handle(self, db, unit_id: UUID) -> ShopUnitNode:
        """
        Обработчик выгрузки по нодам
        :param db:
        :param unit_id:
        :return:
        """
        async with db.begin():
            basic_tree = await self.crud_unit.get_first(db, id=unit_id)

        if basic_tree:
            basic_tree = await self.traverse_response_tree(basic_tree)

        return basic_tree
