import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, MetaData, String, ForeignKeyConstraint, DATETIME, DateTime, \
    TIMESTAMP
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

metadata = MetaData()


class UnitType(enum.Enum):
    OFFER = "OFFER"
    CATEGORY = "CATEGORY"


class ShopImportDB(Base):
    __tablename__ = "import"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    update_at = Column(TIMESTAMP(timezone=True), index=True)


class ShopUnitImportDB(Base):
    __tablename__ = "unit_import"
    import_id = Column(Integer, ForeignKey("import.id"), primary_key=True, index=True)
    id = Column(UUID(as_uuid=True), ForeignKey('unit.id', ondelete="CASCADE"), primary_key=True, index=True)
    type = Column(Enum(UnitType), nullable=False)
    name = Column(String(256), nullable=False)
    price = Column(Integer, nullable=True)
    parentId = Column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    updateDate = Column(TIMESTAMP(timezone=True), index=True)


class ShopUnitDB(Base):
    __tablename__ = "unit"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    type = Column(Enum(UnitType), nullable=False)
    name = Column(String(256), nullable=False)
    price = Column(Integer, nullable=True)
    parentId = Column(
        UUID(as_uuid=True), ForeignKey('unit.id', ondelete="CASCADE"), nullable=True, index=True
    )
    updateDate = Column(TIMESTAMP(timezone=True), index=True)
    children = relationship("ShopUnitDB", lazy="selectin", join_depth=10)

