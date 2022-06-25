from uuid import UUID

from app.schema.schemas import ShopUnitImportRequest, ShopUnitImport, ShopUnitCreate
from fastapi.encoders import jsonable_encoder
from app.db.model import import_tbl, unit_import_tbl, unit_tbl
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncTransaction
from typing import Dict, List
from datetime import datetime


class CRUDUnit:
    MAX_UNIT_IMPORT_PER_INSERT = 32767 // len(unit_import_tbl.columns)

    #    def __init__(self, connection):
    #        self.conn = connection

    @classmethod
    def generate_unit_imports(cls, import_id: int, update_date: datetime, items: List[ShopUnitImport]) -> Dict:
        for item in items:
            yield {
                'import_id': import_id,
                'id': item.id,
                'name': item.name,
                'price': item.price,
                'type': item.type,
                'parent_id': item.parentId,
                'updated_at': update_date
            }

    @classmethod
    def make_chunks(cls, list_obj: List[Dict], n) -> List:

        for i in range(0, len(list_obj), n):
            yield list_obj[i:i + n]

    async def import_create(self, conn: AsyncEngine, data: ShopUnitImportRequest):
        async with conn.begin() as conn:
            query = import_tbl.insert().returning(import_tbl.c.id)
            res = await conn.execute(query)
            import_id = res.scalar()

            update_date = data.updateDate
            items = data.items

            import_rows = list(self.generate_unit_imports(import_id, update_date, items))

            chunked_import_rows = self.make_chunks(import_rows,
                                                   self.MAX_UNIT_IMPORT_PER_INSERT)

            await self.update_units(conn, import_rows)

            query = unit_import_tbl.insert()
            for chunk in chunked_import_rows:
                await conn.execute(query.values(list(chunk)))

            return import_id

    async def update_units(self, conn: AsyncTransaction, import_rows):

        for row in import_rows:
            unit_id = row['id']
            res = await conn.execute(unit_tbl.select().where(unit_tbl.c.id == unit_id))
            exists = len(res.fetchall()) != 0
            # row_to_insert = list(row.values())[1:]

            if exists:
                query = (unit_tbl.update().where(unit_tbl.c.id == row['id']).values(id=row['id'],
                                                                                    name=row['name'],
                                                                                    type=row['type'],
                                                                                    price=row['price'],
                                                                                    parent_id=row['parent_id'],
                                                                                    updated_at=row['updated_at']))
                await conn.execute(query)

            else:
                query = unit_tbl.insert()
                await conn.execute(query.values(id=row['id'],
                                                name=row['name'],
                                                type=row['type'],
                                                price=row['price'],
                                                parent_id=row['parent_id'],
                                                updated_at=row['updated_at']))

    async def delete_unit(self, conn: AsyncEngine, id: UUID):

        async with conn.begin() as conn:
            query = unit_tbl.delete().where(unit_tbl.c.id == id)
            return await conn.execute(query)


