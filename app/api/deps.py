from typing import Generator

# from app.crud.unit_crud_old import ImportCrudHandler
from app.db.db import engine
#from app.db.model import ShopUnitDB, ShopImportDB

from app.crud.crud_unit import CRUDUnit


async def get_eng() -> Generator:
    try:
        yield engine
    finally:
        await engine.dispose()


async def get_import_crud() -> CRUDUnit:
    return CRUDUnit()


