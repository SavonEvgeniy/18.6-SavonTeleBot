import telebot #импорт библиотеки
from config import keys, TOKEN #из файла конфиг импортируем валюты и токен
from extensions import APIException, MoneyConverter #из файла экстеншн импортируем классы
bot = telebot.TeleBot(TOKEN) 
@bot.message_handler(commands=['start', 'help']) #описываем работу комманд /help /start
def help(message: telebot.types.Message):
    text= 'Чтобы начать работу введите комманду боту в следующем формате: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)
@bot.message_handler(commands=['values']) #описываем работу комманды /values
def values(message: telebot.types.Message):
    text= 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message): #функция конвертации
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Неверное количество параметров.') #исключение количество параметров не = 3
        quote, base, amount = values
        total_base = MoneyConverter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base*float(amount)}'
        bot.send_message(message.chat.id, text)
bot.polling()
