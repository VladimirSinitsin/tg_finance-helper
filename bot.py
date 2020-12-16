"""
Основной тестовый файл телеграм бота: t.me/CuteBudgetBot
"""
# import telebot
# from telebot import types
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

import DBMS
import time
from bot_config import TOKEN


# Инициализация бота.
bot = Bot(token=TOKEN)
dp =  Dispatcher(bot)
# Словарь для хранения продуктов и их стоимостей.
products = {}


@dp.message_handler(commands=['start'])
async def send_welcome(message):
    # содание клавиатуры с кнопками
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = KeyboardButton("/start")
    item2 = KeyboardButton("/help")
    item3 = KeyboardButton("/all")
    markup.add(item1, item2, item3)
    await message.answer( 'Привет! Я бот для ведения бюджета\n''' +
                          'Вводи свои покупки в виде: название - цена\n' +
                          'Например: бананы - 300\n\n'
                          'Доступные команды:\n/start\n/help\n/all', reply_markup=markup)


@dp.message_handler(commands=['help'])
async def send_help(message):
    await message.answer('Если тебе нужна помощь, то обратись к разработчикам')


# ВЫвод всех покупок и сумм через /all.
@dp.message_handler(commands=['all'])
async def preview_all_products(message):
    global products
    if products:
        result = ''
        # Записываем все товары и их суммы в строку для вывода.
        for key, value in products.items():
            result += '{0}: {1}\n'.format(key, value)
        await message.answer('Всё покупки:\n\n' + result)
    else:
        await message.answer('Покупок не было')


# Добавление покупки.
@dp.message_handler(content_types=["text"])
async def echo_product(message):
    # клавиатура связанная с бд
    category_callback = CallbackData('Category', 'Name_category')
    markup = InlineKeyboardMarkup(row_width=1)
    for items in DBMS.all_categories():
        item = InlineKeyboardButton(items, callback_data=f"Category:{items}")
        markup.add(item)

    item = InlineKeyboardButton('Новая категория', callback_data="Category:new")
    markup.add(item)
    # item1 = types.InlineKeyboardButton('🍎Продукты🍎', callback_data='Продукты')
    # item2 = types.InlineKeyboardButton('👔Одежда👔', callback_data='Одежда')
    # item3 = types.InlineKeyboardButton('🧮Счета🧮', callback_data='Счета')
    # item4 = types.InlineKeyboardButton('🚘Автомобиль🚘', callback_data='Автомобиль')
    # item5 = types.InlineKeyboardButton('🏄Досуг🏄', callback_data='Досуг')
    # item6 = types.InlineKeyboardButton('❓Прочее❓', callback_data='Прочее')
    # markup.add(item1, item2, item3, item4, item5, item6)

    global products


    # Если уже был, то просто суммируем, иначе создаем новый товар в словаре.
    # if name_of_product in products:
    #     products[name_of_product] += value
    #     value = products[name_of_product]
    # else:
    #     products[name_of_product] = value
    #     bot.reply_to(message, 'К какой категории добавить "' + message.text + '"?🤔', reply_markup=markup)
    # bot.reply_to(message, 'Добавлен товар: {0}\nна сумму: {1}'.format(name_of_product, value))

    # связь бота с базой данных
    # product = DBMS.product_exist(message.text)
    # if product.category == None:
    await message.reply(message, 'Выберите категорию', reply_markup=markup)


# # работа с категориями
# @dp.callback_query_handler()
# async def answer(call, message):
#     if call.data == 'new':
#         await message.reply(message, 'Введите категорию')
#     else:
#         product.category = call.data
#
#
# # метод позволяющий ответить боту
# async def next_step(message):
#     global product
#     try:
#         categoria = message.text
#         product.category = categoria
#     except Exception as e:
#         await message.reply(message, 'Что то пошло не так')


if __name__ == '__main__':
    executor.start_polling(dp)

