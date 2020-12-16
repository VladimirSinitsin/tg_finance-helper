import DBMS


###############
### Расходы ###
###############

#%% Создаем сообщение.
raw_message = 'Бананы - 150'
# Проверка на наличие такого продукта в БД.
product = DBMS.product_exist(raw_message)
# Если БД пустая, то вернётся товар с полем category=None.
print(product)


#%% Добавляем категорию для данного товара в его поле.
product.category = 'Продукты'
# И записываем её в БД.
# При записи также добавится сам товар и расход по нему.
DBMS.add_category(product)


#%% Ещё пример.
raw_message = 'Бензин - 1000'
product = DBMS.product_exist(raw_message)
if not product.category:
    product.category = 'Автомобиль'
DBMS.add_category(product)


#%% Если категория данного товара нам уже известа,
# метод product_exist добавит новый расход по данному товару в БД,
# и вернёт товар с его категорией (category='Продукты').
raw_message = 'Бананы - 150'
product = DBMS.product_exist(raw_message)

print(product)


#%% Если категория уже в БД, но продукт - нет.
raw_message = 'Клубника - 200'
product = DBMS.product_exist(raw_message)
if not product.category:
    product.category = 'Продукты'
DBMS.add_product(product)


#%% Вывод всех категорий при помощи метода all_categories.
print('Все категории:')
[print(category) for category in DBMS.all_categories()]


#%% Вывод всех расходов по категориям.
print(DBMS.db.all_categories_costs())


##############
### Доходы ###
##############

#%% Создаем сообщение.
raw_message = 'Валера - 18000'


#%% Добавляем доход в БД.
# Если вкладчика нет, то создаётся новый, либо добавляется новый доход к существующему.
DBMS.add_deposit(raw_message)


#%% Вывод всех вкладчиков при помощи метода all_depositors.
print('Все вкладчики:')
[print(depositor) for depositor in DBMS.all_depositors()]
