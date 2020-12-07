from .classes import Deposit
from .db import get_cursor
from .db import insert as db_insert
from .tools import get_now_formatted


def add_deposit(raw_message: str) -> None:
    """
    Добавляет доход в БД по сообщению.
    :param raw_message: сообщение.
    """
    deposit = _parse_message(raw_message)
    # Проверяем наличие вкладчика в БД.
    cursor = get_cursor()
    cursor.execute(f"SELECT codename "
                   f"FROM Budget "
                   f"WHERE codename = '{deposit.name}'")
    row = cursor.fetchone()
    # Если вкладчика нет, то добавляем его в БД по имени.
    if not row:
        _add_depositor(deposit)
    # Добавляем доход в БД.
    _add_deposit(deposit)


def _add_depositor(deposit: Deposit) -> None:
    """
    Добавляет вкладчика в БД по доходу.
    :param deposit: доход.
    """
    db_insert("Budget", {"codename": deposit.name})


def _add_deposit(deposit: Deposit) -> None:
    """
    Добавляет доход в БД.
    :param deposit: доход.
    """
    db_insert("Deposit",
              {"money": deposit.money,
               "created": get_now_formatted(),
               "depositor_name": deposit.name})


def _parse_message(raw_message: str) -> Deposit:
    # TODO: Надо реализовать парсер сообщений с доходом.
    text = raw_message.split()
    return Deposit(name=text[0], money=float(text[1]))
