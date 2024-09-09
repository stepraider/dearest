from flask import Flask, request
import telebot
import os

API_TOKEN = os.getenv('7199720833:AAF_ICtH8t17NyQlftUeoJg8Kzm27gQlQGE')  # Токен из BotFather
bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)

# Приветственное сообщение
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать в бот!")

# Эхо-сообщение — бот отвечает тем же текстом
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

# Обработчик вебхука
@server.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    json_str = request.stream.read().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

# Настройка вебхука
@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://dvatest.herokuapp.com/' + API_TOKEN)
    return "Webhook set!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
