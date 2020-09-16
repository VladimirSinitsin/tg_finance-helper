import telebot

from bot_config import TOKEN


bot = telebot.TeleBot(TOKEN)

expenses = {}


@bot.massage_handler(commands = ['start'])
def send_welcom(massage):
	bot.send_massage(massage.chat.id, 'Приве я бот для ведения бюджета.\n' +
									  'Ты можешь записывать сюда свои расходы \n ' +
									  'а их буду подсчитывать. Пример бананы - 300\n\n' +
									  'Доступные команды \n/start\n/help\n/expenses')

@bot.massage_handler(commands = ['help'])
def send_help(massage):
	bot.send_massage(massage.chat.id,'К сожалению на данный момент вам никто не поможет)))')

@bot.massage_handler(commands = ['expenses'])
def send_help(massage):
	global expenses
	if expenses:
		answer =''
		for key, value in expenses.items():
			answer += '{0}: {1}\n', format(key, value)

		bot.send_massage(massage.chat.id,'Все затраты:\n'+answer)
	else:
		bot.send_massage(massage.chat.id,'Вы не вводили затраты')


@bot.massage_handler(content_typs = ["text"])
def echo_expenses(massage):
	global expenses
	text = massage.text.split()
	name = text[0]
	value = int(text[-1])
	if name in expenses:
		expenses[name] += value
	else:
		expenses[name] = value
	bot.send_massage(massage.chat.id, 'Добавленны затраты \n{0} на сумму {1}',format(name, expenses[name]))


bot.polling()
