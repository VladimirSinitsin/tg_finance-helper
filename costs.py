from typing import NamedTuple, Optional
import datetime
import pytz

from products import Product
import db


TIME_ZONE = 'Europe/Moscow'


def add_cost(product: Product) -> Product:
    """
    Добавляет трату в БД.
    :param product: товар.
    :return: добавленный товар.
    """
    db.insert("Cost",
              {"price": product.price,
               "created": _get_now_formatted(),
               "product_codename": product.codename})
    return product


def _get_now_formatted() -> str:
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    tz = pytz.timezone(TIME_ZONE)
    now = datetime.datetime.now(tz)
    return now
