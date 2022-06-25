from app.schema.schemas import ShopImportCreate, ShopUnitCreate, ShopUnitImport
#from app.db.model import ShopImportDB


def generate_unit_imports(id: int, item: ShopUnitImport)-> ShopUnitCreate:
    return ShopUnitCreate(
        import_id=id,
        unit_id=item.id,
        name=item.name,
        price=item.price,
        type=item.type,
        parentId = item.parentId,
    )

async def handle_import(db, crud_unit, crud_import, data):


    import_obj = ShopImportCreate(
        update_date= data.updateDate
    )


    db_obj = ShopImportDB(**import_obj.dict())

    obj_added = await crud_import.create(db, data=db_obj)

    db.refresh(obj_added)

    import_id = obj_added.id

    return obj_added

"""
    for item in data.items:

        obj_unit = generate_unit_imports(import_id, item)

        obj_unit_in = ShopUnitDB(**obj_unit.dict())

        added_obj = await crud_unit.create(db, data=obj_unit_in)

    return obj_added

"""