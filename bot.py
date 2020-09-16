import telebot

from bot_config import TOKEN


bot = telebot.TeleBot(TOKEN)

expenses = {}


@bot.message_handler(commands = ['start'])
def send_welcom(message):
	bot.send_message(message.chat.id, 'Приве я бот для ведения бюджета.\n' +
									  'Ты можешь записывать сюда свои расходы \n ' +
									  'а их буду подсчитывать. Пример бананы - 300\n\n' +
									  'Доступные команды \n/start\n/help\n/expenses')

@bot.message_handler(commands = ['help'])
def send_help(message):
	bot.send_message(message.chat.id,'К сожалению на данный момент вам никто не поможет)))')

@bot.message_handler(commands = ['expenses'])
def send_help(message):
	global expenses
	if expenses:
		answer =''
		for key, value in expenses.items():
			answer += '{0}: {1}\n', format(key, value)

		bot.send_message(message.chat.id,'Все затраты:\n'+answer)
	else:
		bot.send_message(message.chat.id,'Вы не вводили затраты')


@bot.message_handler(content_typs = ["text"])
def echo_expenses(message):
	global expenses
	text = message.text.split()
	name = text[0]
	value = int(text[-1])
	if name in expenses:
		expenses[name] += value
	else:
		expenses[name] = value
	bot.send_message(message.chat.id, 'Добавленны затраты \n{0} на сумму {1}',format(name, expenses[name]))


bot.polling()
