import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, MetaData, String, ForeignKeyConstraint, DATETIME, DateTime, \
    TIMESTAMP
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from app.db.session import Base
from sqlalchemy import func, DDL

metadata = MetaData()


class UnitType(enum.Enum):
    OFFER = "OFFER"
    CATEGORY = "CATEGORY"


class ShopImportDB(Base):
    """
    Таблица для ведения учетов выгрузки (инкремента)
    """
    __tablename__ = "import"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    update_date = Column(TIMESTAMP(timezone=True), index=True)


class ShopUnitImportDB(Base):
    """
        Таблица для формирования базы покупок+импортов
    """
    __tablename__ = "unit_import"

    import_id = Column(Integer, ForeignKey("import.id"), primary_key=True, index=True)
    id = Column(UUID(as_uuid=True), ForeignKey('unit.id', ondelete="CASCADE"), primary_key=True, index=True)
    type = Column(Enum(UnitType), nullable=False)
    name = Column(String(256), nullable=False)
    price = Column(Integer, nullable=True)
    parentId = Column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    update_date = Column(TIMESTAMP(timezone=True), index=True)


class ShopUnitDB(Base):
    """
    Таблица для ведения актуальной базы покупки
    """
    __tablename__ = "unit"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    type = Column(Enum(UnitType), nullable=False)
    name = Column(String(256), nullable=False)
    price = Column(Integer, nullable=True)
    parentId = Column(
        UUID(as_uuid=True), ForeignKey('unit.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=True, index=True
    )
    update_date = Column(TIMESTAMP(timezone=True), index=True)
    children = relationship("ShopUnitDB", lazy="selectin", join_depth=10)

func = DDL(
    """
    create or replace procedure compute_parent_mean(
   parent_id uuid
)
language plpgsql
as $$
begin
    -- subtracting the amount from the sender''s account
    update unit
    set price = c.child_price, update_date = updated
    from (select "parentId",
                 max(update_date) as updated,
                 avg(price) as child_price
          from unit
          where "parentId" = parent_id
          group by "parentId") c
    where id = c."parentId";
    commit;
end;$$
"""
)