from app.crud.base import CRUDBase
from app.model.unit_model import ShopUnitDB, ShopImportDB
from app.schema.schemas import ShopUnitCreate, ShopImportCreate


class UnitCRUD(CRUDBase[ShopUnitDB, ShopUnitCreate, ShopUnitCreate]):
    pass


class ImportCRUD(CRUDBase[ShopImportDB, ShopImportCreate, ShopImportCreate]):
    pass
