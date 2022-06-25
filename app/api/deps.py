from typing import Generator

# from app.crud.unit_crud_old import ImportCrudHandler
from app.db.session import SessionLocal
from app.model.db_models import ShopUnitDB, ShopImportDB, ShopUnitImportDB
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_unit import CRUDUnit, CRUDImport, CRUDUnitImport
from app.api.handlers.import_handler import HandlerImport


async def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    finally:
        await db.close()


def get_import_crud() -> CRUDImport:
    return CRUDImport(ShopImportDB)


def get_unit_import_crud() -> CRUDUnitImport:
    return CRUDUnitImport(ShopUnitImportDB)


def get_unit_crud() -> CRUDUnit:
    return CRUDUnit(ShopUnitDB)


async def get_import_handler() -> HandlerImport:
    return HandlerImport(get_import_crud(), get_unit_import_crud(), get_unit_crud())
