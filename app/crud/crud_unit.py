from app.crud.base import CRUDBase
from app.models.unit import Unit
# from app.schemas. import RecipeCreate, RecipeUpdate


class CRUDUnit(CRUDBase[Unit, ShopUnitCreate, ShopUnitUpdate, ShopUnit]):
    ...


unit = CRUDUnit(Unit)