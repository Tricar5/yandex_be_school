from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

engine = create_async_engine(
    URL.create(
    drivername="postgresql+asyncpg",
    host=settings.DATABASE_HOST,
    database=settings.DATABASE_NAME,
    username=settings.DATABASE_USERNAME,
    password=settings.DATABASE_PASSWORD,
    port=settings.DATABASE_PORT,
    ),
    echo=True,
)

# Base
Base = declarative_base()

# Session


SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


"""
    import_obj = ShopImportCreate(
        update_date=data.updateDate
    )

    enc_obj = jsonable_encoder(import_obj)

    db_obj = ShopImportDB(**import_obj.dict())

    db_obj = await crud_import.create(db, data=db_obj)

    import_id = db_obj.id

    print(db_obj)

    for item in data.items:
        obj_unit_in = generate_unit_imports(import_id, item)

        added_obj = await crud_import.create(db, obj_unit_in)

    return added_obj
"""