from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = "postgresql://app:temp_pwd@127.0.0.1:5432/yandex"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
