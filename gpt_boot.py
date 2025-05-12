from flask import Flask, request
import telebot
import openai
import os

# Получаем токены из переменных окружения
BOT_TOKEN = os.getenv("")
OPENAI_API_KEY = os.getenv("")

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# Создаём Flask-сервер
app = Flask(__name__)

# Обрабатываем команды Telegram
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я GPT-бот на базе модели GPT-4o.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": message.text}
        ]
    )
    reply = response.choices[0].message.content
    bot.send_message(message.chat.id, reply)

# Обработка входящих сообщений от Telegram через Webhook
@app.route('/', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return '', 200

# Запуск приложения + установка Webhook
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url='https://gpt-alisa-bot.onrender.com')  # ← сюда вставь свой URL Render
    app.run(host="0.0.0.0", port=10000)
