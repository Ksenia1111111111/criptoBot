import telebot
from config import TOKEN, CURRENCY_CODES
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_help(message):
    text = (
        "Чтобы узнать цену валюты, отправьте сообщение в формате:\n"
        "<имя валюты> <в какую валюту> <количество>\n"
        "Например:\nевро доллар 10\n\n"
        "Посмотреть, какие валюты доступны: /values"
    )
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def handle_values(message):
    text = "Доступные валюты:\n"
    for k, v in CURRENCY_CODES.items():
        text += f"{k.title()} ({v})\n"
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def handle_convert(message):
    try:
        parts = message.text.strip().lower().split()
        if len(parts) != 3:
            raise APIException("Неверный формат. Пример: евро доллар 15")

        base, quote, amount = parts
        result = CurrencyConverter.get_price(base, quote, amount)
        answer = f"{amount} {base} = {result} {quote}"
        bot.send_message(message.chat.id, answer)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Внутренняя ошибка:\n{e}")

bot.polling()