"""
Основной тестовый файл телеграм бота: t.me/CuteBudgetBot
"""
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import DBMS
from bot_config import TOKEN


class Statement(StatesGroup):
    answer = State()


# Инициализация бота.
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

# Инициализация глобальных переменных.
product = DBMS.Product("", 0, None)
raw_message = ""


@dp.message_handler(commands=['start'])
async def send_welcome(message):
    # содание клавиатуры с кнопками
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = KeyboardButton("/start")
    item2 = KeyboardButton("/help")
    item3 = KeyboardButton("/all")
    markup.add(item1, item2, item3)
    await message.answer('Привет! Я бот для ведения бюджета\n'
                         'Вводи свои покупки в виде: название - цена\n'
                         'Например: бананы - 300\n\n', reply_markup=markup)


@dp.message_handler(commands=['help'])
async def send_help(message):
    await message.answer('Если тебе нужна помощь, то обратись к разработчикам.\n'
                         'Ниже приведён список команд для очистки: '
                         '/delete_costs - удалить все расходы\n'
                         '/delete_deposits - удалить все доходы\n'
                         '/delete_costs_deposits - удалить все доходы и расходы\n'
                         '/delete_db - очистить всю базу данных')


@dp.message_handler(commands=['all'])
async def send_help(message):
    answer = DBMS.db.all_categories_costs()
    if answer:
        await message.answer(answer)
    else:
        await message.answer('Расходов не было.')


@dp.message_handler(commands=['delete_db'])
async def send_help(message):
    DBMS.db.delete_db()
    await message.answer('База данных полностью очищена')


@dp.message_handler(commands=['delete_costs'])
async def send_help(message):
    DBMS.db.delete_costs()
    await message.answer('Все расходы удалены')


@dp.message_handler(commands=['delete_deposits'])
async def send_help(message):
    DBMS.db.delete_deposits()
    await message.answer('Все доходы удалены')


@dp.message_handler(commands=['delete_costs_deposits'])
async def send_help(message):
    DBMS.db.delete_deposits()
    DBMS.db.delete_costs()
    await message.answer('Все доходы и расходы удалены')


# Основной вопрос: доход/расход.
@dp.message_handler(content_types=["text"])
async def echo_product(message):
    global product
    global raw_message

    raw_message = message.text

    try:
        product = DBMS.product_exist(raw_message)
    except Exception as e:
        await message.answer(f"Что-то пошло не так: {e}")
    else:
        if product.category:
            await message.answer(f"Товар {product.codename} на сумму {product.price} "
                                 f"добавлен в категорию {product.category}.")
        else:
            # Клавиатура с выбором.
            keyboard = InlineKeyboardMarkup(row_width=2)
            deposit = InlineKeyboardButton("Доход", callback_data="Доход")
            cost = InlineKeyboardButton("Расход", callback_data="Расход")
            keyboard.add(deposit, cost)

            # Далее обработка ответа.
            await message.answer('Это доход или расход', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'Доход')
async def process_callback_button1(callback_query: types.CallbackQuery):
    global raw_message

    try:
        deposit = DBMS.add_deposit(raw_message)
    except Exception as e:
        await bot.send_message(callback_query.message.chat.id, f"Что-то пошло не так: {e}")
    else:
        await bot.send_message(callback_query.message.chat.id, f"Депозит от {deposit.name} "
                                                               f"на сумму {deposit.money} был добавлен.")


@dp.callback_query_handler(lambda c: c.data == 'Расход')
async def process_callback_button1(callback_query: types.CallbackQuery):
    global product
    # Известные категории из БД.
    markup = InlineKeyboardMarkup(row_width=1)
    for items in DBMS.all_categories():
        item = InlineKeyboardButton(items, callback_data=items)
        markup.add(item)
    # Выбор новой.
    item = InlineKeyboardButton('Новая категория', callback_data="new")
    markup.add(item)

    await bot.send_message(callback_query.message.chat.id, 'Выбери категорию:', reply_markup=markup)


# Если была выбрана уже известная категория.
@dp.callback_query_handler(lambda c: c.data in DBMS.all_categories())
async def process_callback_button1(callback_query: types.CallbackQuery):
    global product
    product.category = callback_query.data
    DBMS.add_product(product)
    await bot.send_message(callback_query.message.chat.id,
                           f"Товар {product.codename} на сумму {product.price} "
                           f"добавлен в категорию {product.category}.")


# Если была выбрана новая категория.
@dp.callback_query_handler(lambda c: c.data == 'new')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await Statement.answer.set()
    await bot.send_message(callback_query.message.chat.id, "Введите новую категорию")


# Изменение состояния для ввода ответа. Добавление новой категории и товара.
@dp.message_handler(state=Statement.answer)
async def process_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        user_message = data['text']
        product.category = user_message
        DBMS.add_category(product)
        await message.answer(f"Товар {product.codename} на сумму {product.price} "
                             f"добавлен в категорию {product.category}.")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
