from typing import Generator

from app.crud.unit_crud import UnitCRUD
from app.db.session import SessionLocal
from app.model.db_unit import DBShopUnit


async def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    finally:
        await db.close()


async def get_user_crud() -> UnitCRUD:
    return UnitCRUD(DBShopUnit)
