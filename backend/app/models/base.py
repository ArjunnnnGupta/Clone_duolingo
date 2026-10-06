from typing import Any

from sqlalchemy import JSON, MetaData, Text
from sqlalchemy.orm import DeclarativeBase

# Explicit names make constraint errors readable and keep `.schema` output stable.
NAMING_CONVENTION = {
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)
    # The schema doc uses TEXT throughout; SQLite would otherwise get VARCHAR.
    type_annotation_map = {str: Text, dict[str, Any]: JSON}


def sql_in_list(values: tuple[str, ...] | tuple[int, ...]) -> str:
    """Render values for a CHECK ... IN (...) clause, e.g. ('a', 'b') -> "'a', 'b'"."""
    return ", ".join(repr(value) for value in values)
