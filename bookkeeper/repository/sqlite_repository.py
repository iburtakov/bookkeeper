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

    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        self.obj_cls = cls

    def add(self, obj: T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        names = ', '.join(self.fields.keys())
        questions = ', '.join("?" * len(self.fields))
        values = [getattr(obj, f) for f in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES({questions})',
                values
            )
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk
    
    def _row2obj(self, rowid: int, row: tuple[Any]) -> T:
        """ Конвертирует строку из БД в объект типа Т """
        kwargs = dict(zip(self.fields, row))
        obj = self.obj_cls(**kwargs)
        obj.pk = rowid
        return obj