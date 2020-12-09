import DBMS


#%% Создаем сообщение (пока строго типизированное).
raw_message = 'Бананы 150'
# Проверка на наличие такого продукта в БД.
product = DBMS.product_exist(raw_message)
# Если БД пустая, то вернётся товар с полем category=None.
print(product)


#%% Добавляем категорию для данного товара в его поле.
product.category = 'Продукты'
# И записываем её в БД.
# При записи также добавится сам товар и расход по нему.
DBMS.add_category(product)


#%% Когда категория данного товара нам уже известа,
# метод product_exist добавит новый расход по данному товару в БД,
# и вернёт товар с его категорией (category='Продукты').
raw_message = 'Бананы 150'
product = DBMS.product_exist(raw_message)

print(product)
