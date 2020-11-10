from typing import NamedTuple, Optional, List

from products import Product, add_product
import db


def add_category(product: Product) -> Product:
    """
    Добавляет категорию в БД.
    :param product: товар, у котого указана категория.
    :return: добавленный товар.
    """
    db.insert("Category", {"category_codename": product.category})
    return add_product(product)


def all_categories() -> List[str]:
    """
    Возвращает все категории.
    :return: список с названиями категорий.
    """
    result_rows = db.fetchall("Category", ["category_codename"])
    result = []
    for row in result_rows:
        result.append(row['category_codename'])
    return result
