from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings
from app.db.model import metadata

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

metadata = metadata
