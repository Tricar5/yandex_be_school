import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, MetaData, String
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

metadata = MetaData()


class UnitType(enum.Enum):
    OFFER = "OFFER"
    CATEGORY = "CATEGORY"


class DBShopUnitImports(Base):
    __tablename__ = "imports"
    import_id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    update_date = Column(TIMESTAMP)


class DBShopUnit(Base):
    __tablename__ = "units"
    import_id = Column(Integer, ForeignKey("imports.import_id"))
    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, index=True)
    type = Column(Enum(UnitType), nullable=False)
    name = Column(String(256), nullable=False)
    price = Column(Integer, nullable=True)
    parentId = Column(
        UUID(as_uuid=True), ForeignKey("units.id"), nullable=True, index=True
    )
    children = relationship("DBShopUnit", remote_side=[id])
