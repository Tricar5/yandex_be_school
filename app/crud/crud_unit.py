from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.crud.base import Session
from app.model.db_unit import DBShopUnit, DBShopUnitImports  # , dbShopUnitRelations
from app.schema.schemas import ShopUnitImportRequest


def create_units(db: Session, obj_in: ShopUnitImportRequest) -> Optional:

    items = obj_in.items
    new_import = DBShopUnitImports(update_date=obj_in.updateDate)

    db.add(new_import)

    increment = db.query(func.max(DBShopUnitImports.import_id))
    for item in items:

        obj_unit = jsonable_encoder(item)
        new_unit = DBShopUnit(import_id=increment, **obj_unit)
        # new_relation = dbShopUnitRelations(import_id=increment, unit_id=item.id, parentId=item.parentId)
        db.add(new_unit)
    # db.add(new_relation)

    db.commit()
    print(new_unit)
    return increment
