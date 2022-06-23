import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, MetaData, String, ForeignKeyConstraint, DATETIME, DateTime, TIMESTAMP
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

metadata = MetaData()


class UnitType(enum.Enum):
    OFFER = "OFFER"
    CATEGORY = "CATEGORY"


class ShopImportDB(Base):
    __tablename__ = "import"
    id = Column(Integer,  primary_key=True, index=True)
    update_date = Column(TIMESTAMP(timezone=True), index=True)


class ShopUnitDB(Base):
    __tablename__ = "unit"

    __tableargs__ = (ForeignKeyConstraint(["unit.import_id", "unit.parent_id"],
                                           ["unit.import_id", "unit.unit_id"]),
                     ForeignKeyConstraint(["unit.import_id", "unit.unit_id"],
                                        ["unit.import_id", "unit.parent_id"])
                     )

    import_id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    type = Column(Enum(UnitType), nullable=False)
    name = Column(String(256), nullable=False)
    price = Column(Integer, nullable=True)
    parent_id = Column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    """
    parent = relationship('ShopUnitDB',
                          cascade="all,delete,delete-orphan",
                          primaryjoin="unit.import_id == unit.import_id and unit.unit_id == unit.parent_id",
                          foreign_keys = [import_id, parent_id],
                          remote_side = [import_id, unit_id])
    children = relationship('ShopUnitDB', backref="parent",)
    """