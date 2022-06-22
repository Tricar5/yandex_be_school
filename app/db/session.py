from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    future=True,
)

# Base
Base = declarative_base()

# Session
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
