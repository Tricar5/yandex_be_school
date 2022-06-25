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
