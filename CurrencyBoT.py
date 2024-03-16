import telebot
from Cb_token import keys, TOKEN
from Cb_class import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.reply_to(message, "Привет!\nЧтобы узнать больше, нажми на /help")


#Напишем обработчик, который будет обрабатывать команду /help,
# после которой будет выводиться инструкция по применению бота:
@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    bot.reply_to(message, "Чтобы начать работу, введите значения в формате:\n-название валюты;\n-в какую валюту перевести;\n-количество переводимой валюты;\n- команда /values выдаст список доступных валют.")


#Напишем обработчик, который будет реагировать на команду /values,
# и будет выводить доступные валюты:
@bot.message_handler(commands=['values'])
def value(message: telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

#Напишем обработчик, который конвертирует валюты:
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        # Формируем исключение - если валюты равны друг друг (доллар=доллару, биткоин=биткоину и т.д.):
        if len(values) != 3:
            raise ConvertionException("Слишком много параметров!\nВведите значение ещё раз")

        #биткоин(quote - валюта, КОТОРУЮ мы хотим конвертировать), доллар(base - валюта, В КОТОРУЮ нужно конвертировать), 1(ammount - количество валюты, КОТОРУЮ мы хотим конвертировать)
        quote, base, ammount = values
        total_base = CryptoConverter.convert(quote, base, ammount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n {e}')

    else:
        text = f'Цена {ammount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)


















