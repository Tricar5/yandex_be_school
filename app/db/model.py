from enum import Enum, unique

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    DDL, ForeignKeyConstraint,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID, ENUM


convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}



metadata = MetaData(convention)

class UnitType(Enum):
    OFFER = "OFFER"
    CATEGORY = "CATEGORY"

import_tbl = Table(
                "import",
                metadata,
                Column('id', Integer, primary_key=True, nullable=False, index=True))


unit_import_tbl = Table(
                "unit_import",
                metadata,
                Column('import_id', Integer, ForeignKey('import.id'), primary_key=True, nullable=False, index=True),
                Column('id', UUID(as_uuid=True), ForeignKey('unit.id', ondelete="CASCADE"), primary_key=True,
                       nullable=False, index=True),
                Column('type', ENUM(UnitType, name='unit_type'), nullable=False),
                Column('name', String(256), nullable=False),
                Column('price', Integer, nullable=True),
                Column('parent_id', UUID(as_uuid=True), nullable=True, index=True),
                Column('updated_at', TIMESTAMP(timezone=True), nullable=False, index=True),
                #ForeignKeyConstraint(['import_id', 'parent_id'],
                #            ['unit_import.import_id', 'unit_import.id'], ondelete="CASCADE")

)


unit_tbl = Table(
    'unit',
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, nullable=False, index=True),
    Column('type', ENUM(UnitType, name='unit_type'), nullable=False),
    Column('name', String(256), nullable=False),
    Column('price', Integer, nullable=True),
    Column('parent_id', UUID(as_uuid=True), ForeignKey('unit.id', ondelete='CASCADE'), nullable=True, index=True),
    Column('updated_at', TIMESTAMP(timezone=True), nullable=False),
)