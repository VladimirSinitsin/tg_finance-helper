import os
from typing import Dict, List, Tuple

import sqlite3


# Подключение к БД.
conn = sqlite3.connect(os.path.join("finance.db"))
cursor = conn.cursor()


def insert(table: str, column_values: Dict):
    """
    Метод реализующий INSERT для БД.
    :param table: название таблицы.
    :param column_values: столбцы для вставки и значения.
    """
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def delete_cost(table: str, id: int) -> None:
    """
    Метод реализующий DELETE для расхода по его id в БД.
    :param table: название таблицы.
    :param id: id записи, которую нужно удалить.
    """
    cursor.execute(f"DELETE FROM {table} WHERE id={id}")
    conn.commit()


def fetchall(table: str, columns: List[str]) -> List[Dict]:
    """
    Все записи из конкретных столбцов таблицы.
    :param table: название таблицы.
    :param columns: список нужных столбцов.
    :return: список словарей-строк, в котором ключ - название столбца.
    """
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def get_cursor():
    return cursor


def delete_db():
    os.remove("finance.db")


def _init_db():
    """
    Создание таблиц в БД (выполняется скрипт 'createdb.sql').
    """
    with open("./DBMS/createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """
    Проверка на наличие таблиц в БД через таблицу 'sqlite_master'.
    В случае отстутсвия создаются.
    """
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='Budget'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()
