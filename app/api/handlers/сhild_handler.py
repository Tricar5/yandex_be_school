from uuid import UUID

from fastapi.encoders import jsonable_encoder
from typing import Dict, Generator, Union
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from app.schema.schemas import ShopUnitImportSchema, ShopImportSchema, ShopUnitSchema
from app.schema.request import ShopUnitImport, ShopUnitImportRequest
from app.schema.response import ShopUnitNode
from app.model.db_models import ShopImportDB, ShopUnitDB, ShopUnitImportDB
from app.crud.crud_unit import CRUDUnitImport, CRUDImport, CRUDUnit


# from sqlalchemy import exists, select


class HandlerChildren:
    def __init__(self, crud_unit: CRUDUnit):
        self.crud_unit = crud_unit


    async def traverse_response_tree(self, d):

        """
        Трассировка и форматирования nested дерева из базы
        :param d: Результ lazyloading с помощью ORM модели
        :return:
        """
        if len(d['children']) == 0:
            return {'id': d['id'],
                    'name': d['name'],
                    'parentId': d['parentId'],
                    'price': d['price'],
                    'type': d['type'],
                    'updateDate': d['updateDate']}

        return {'id': d['id'],
                'name': d['name'],
                'parentId': d['parentId'],
                'price': sum(
                    [children['price'] if type(children['price']) is int else 0 for children in d['children']]) / len(
                    [children['price'] if type(children['price']) is int else 0 for children in d['children']]),
                'type': d['type'],
                'updateDate': d['updateDate'],
                'children': [self.traverse_response_tree(children) for children in d['children']]}

    async def handle(self, db, unit_id: UUID) -> ShopUnitNode:
        """
        Обработчик выгрузки по нодам
        :param db:
        :param unit_id:
        :return:
        """
        async with db.begin():
            basic_tree = await self.crud_unit.get_first(db, id=unit_id)

        res = await self.traverse_response_tree(basic_tree)

        return res
