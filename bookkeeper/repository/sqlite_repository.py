"""
Модуль описывает репозиторий, работающий в БД SQLite
"""

from typing import Any
from inspect import get_annotations
import sqlite3

from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SQLiteRepository(AbstractRepository[T]):
    """
    Репозиторий, работающий c базой данных SQLite.
    """
    db_file: str
    table_name: str
    fields: dict[str, Any]
    obj_cls: type