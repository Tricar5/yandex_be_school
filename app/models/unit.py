import typing as t
from sqlalchemy import Integer, String, Column, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, ENUM
from sqlalchemy.orm import relationship

from app.db.base_class import Base

@unique
class UnitType(ENUM):
    category = 'CATEGORY'
    offer = 'OFFER'


class ShopUnitImports(Base):
    import_id = Column(Integer, primary_key=True, index=True)
    #parentId = relationship("Unit",
    #                        cascade="all,delete-orphan",
    #                       remote_side=[import_id])



class ShopUnit(Base):
    import_id = Column(Integer, ForeignKey(ShopUnitImports))
    unit_id = Column(UUID, primary_key=True, index=True)
    unit_type = Column(ENUM(UnitType), nullable=False)
    name = Column(String(256), nullable=False)
    date = Column(TIMESTAMP, nullable=False)
    #parentId = relationship("Unit",
    #                        cascade="all,delete-orphan",
    #                        remote_side=[id])


class ShopUnitRelations(Base):
    import_id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(UUID, index=True)
    parentId = relationship("Relations",
                            cascade="all,delete-orphan",
                            remote_side=[unit_id])