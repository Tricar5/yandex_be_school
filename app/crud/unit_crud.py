from app.crud.base import CRUDBase
from app.model.db_unit import DBShopUnit
from app.schema.schemas import ShopUnitImport


class UnitCRUD(CRUDBase[DBShopUnit, ShopUnitImport, ShopUnitImport]):
    pass
