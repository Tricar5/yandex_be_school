from typing import Generator

# from app.crud.unit_crud_old import ImportCrudHandler
from app.db.session import SessionLocal
from app.model.unit_model import ShopUnitDB, ShopImportDB
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_unit import UnitCRUD, ImportCRUD


async def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    finally:
        await db.close()


async def get_unit_crud() -> UnitCRUD:
    return UnitCRUD(ShopUnitDB)


async def get_import_crud() -> ImportCRUD:
    return ImportCRUD(ShopImportDB)