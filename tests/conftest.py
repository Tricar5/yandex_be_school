import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.core.database import Base
from app.main import app

# TEST PIPELINE
# CREATE DATABASE -> FILL DATABASE WITH DATA -> TEST1 -> DROP DATABASE
#
# CREATE DATABASE -> FILL DATABASE WITH DATA -> TEST2 -> DROP DATABASE
# ...


sync_engine = create_engine(
    URL.create(
        drivername="postgresql",
        host="0.0.0.0",
        database="test_api",  # нужна тестовая бд!
        username="postgres",
        password="postgres",
        port="5432",
    ),
    future=True,
)

SyncSession = sessionmaker(sync_engine, autocommit=False, autoflush=False)


@pytest.fixture()
def setup_db():
    Base.metadata.create_all(bind=sync_engine)
    yield
    Base.metadata.drop_all(bind=sync_engine)


@pytest.fixture()
def put_shopunits_in_db(setup_db):
    session = SyncSession()
    shopunits = [
        # IF YOU WANT FILL THE DATABASE BEFORE TESTS
        # CREATE MODELS HERE LIKE
        # dbShopUnits("Телефоны"),
        # dbShopUnits("m-700"),
        # dbShopUnits("samsung_galaxy"),
    ]
    for shopunit in shopunits:
        session.merge(shopunit)

    session.commit()
    session.flush()
    session.close()


#############################################################################
# dependencies override
#############################################################################


async def get_db_override() -> AsyncSession:
    engine = create_async_engine(
        URL.create(
            drivername="postgresql+asyncpg",
            host="0.0.0.0",
            database="test_api",  # нужна тестовая бд!
            username="postgres",
            password="postgres",
            port="5432",
        ),
        future=True,
        pool_pre_ping=True,
    )

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


app.dependency_overrides[get_db] = get_db_override


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://") as client:
        yield client


# TEST DATA

IMPORT_BATCHES = [
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None,
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z",
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Смартфоны",
                "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            },
            {
                "type": "OFFER",
                "name": "jPhone 13",
                "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "price": 79999,
            },
            {
                "type": "OFFER",
                "name": "Xomiа Readme 10",
                "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "price": 59999,
            },
        ],
        "updateDate": "2022-02-02T12:00:00.000Z",
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Телевизоры",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            },
            {
                "type": "OFFER",
                "name": 'Samson 70" LED UHD Smart',
                "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 32999,
            },
            {
                "type": "OFFER",
                "name": 'Phyllis 50" LED UHD Smarter',
                "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 49999,
            },
        ],
        "updateDate": "2022-02-03T12:00:00.000Z",
    },
    {
        "items": [
            {
                "type": "OFFER",
                "name": 'Goldstar 65" LED UHD LOL Very Smart',
                "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 69999,
            }
        ],
        "updateDate": "2022-02-03T15:00:00.000Z",
    },
]
