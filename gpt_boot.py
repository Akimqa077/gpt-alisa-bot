import telebot
from openai import OpenAI

# 🔐 Подставь сюда свои реальные ключи
TELEGRAM_TOKEN = "7726330072:AAGkhg-8gmZJ2i10_JYIkYnc9YJ7GqJ4IDQ"
OPENAI_API_KEY = "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"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    prompt = message.text
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message.content.strip()
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ GPT Error: {e}")

print("Бот запущен. Ждёт сообщений...")
bot.polling()
