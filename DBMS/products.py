from .classes import Product
from .db import insert, get_cursor
from .costs import add_cost


def product_exist(raw_message: str) -> Product:
    """
    Проверяет есть ли товар в БД.
    :param raw_message: необработанное сообщение.
    :return: товар.
    """
    product = _parse_message(raw_message)
    cursor = get_cursor()
    # Записываем категорию у товара из БД с таким названием.
    cursor.execute(f"SELECT category_codename "
                   f"FROM Product "
                   f"WHERE codename = '{product.codename}'")
    row = cursor.fetchone()
    # Если категория есть, то присваиваем её товару и записываем трату по нему в БД.
    if row:
        product.category = row[0]
        return add_cost(product)
    # Иначе возвращает товар без категории.
    else:
        return product


def add_product(product: Product) -> Product:
    """
    Добавляет товар в БД.
    :param product: товар.
    :return: добавленный товар.
    """
    insert("Product",
           {"codename": product.codename,
            "category_codename": product.category})
    return add_cost(product)


def _parse_message(raw_message: str) -> Product:
    # TODO: Надо реализовать парсер сообщений с товаром.
    text = raw_message.split()
    return Product(codename=text[0], price=float(text[1]), category=None)
