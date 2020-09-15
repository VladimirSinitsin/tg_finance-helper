"""
Основной тестовый файл телеграм бота: t.me/CuteBudgetBot
"""
import telebot

from bot_config import TOKEN


# Инициализация бота.
bot = telebot.TeleBot(TOKEN, parse_mode=None)

# Словарь для хранения продуктов и их стоимостей.
products = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет! Я бот для ведения бюджета\n''' +
                          'Вводи свои покупки в виде: название - цена\n' +
                          'Например: бананы - 300\n\n'
                          'Доступные команды:\n/start\n/help\n/all')


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 'Если тебе нужна помощь, то обратись к разработчикам')


# ВЫвод всех покупок и сумм через /all.
@bot.message_handler(commands=['all'])
def preview_all_products(message):
    global products
    if products:
        result = ''
        # Записываем все товары и их суммы в строку для вывода.
        for key, value in products.items():
            result += '{0}: {1}\n'.format(key, value)
        bot.reply_to(message, 'Всё покупки:\n\n' + result)
    else:
        bot.reply_to(message, 'Покупок не было')


# Добавление покупки.
@bot.message_handler(func=lambda m: True, content_types=["text"])
def echo_product(message):
    global products
    # Разбиваем строку, где 1 элемент - название товара, а последний - его стоимость.
    text = message.text.split()
    name_of_product = text[0]
    value = int(text[-1])
    # Если уже был, то просто суммируем, иначе создаем новый товар в словаре.
    if name_of_product in products:
        products[name_of_product] += value
        value = products[name_of_product]
    else:
        products[name_of_product] = value
    bot.reply_to(message, 'Добавлен товар: {0}\nна сумму: {1}'.format(name_of_product, value))


bot.polling()
