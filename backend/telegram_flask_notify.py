# backend/telegram_flask_notify.py
from flask import Flask, request
from telegram import Bot
import asyncio

TOKEN = "8293900584:AAGnknhlDJzhXo8ZqjwPlZS9irtPBJUm1ZI"
bot = Bot(token=TOKEN)
app = Flask(__name__)

# Добавь сюда chat_ids, которые получили /start
CHAT_IDS = set()

@app.route("/notify", methods=["POST"])
def notify():
    data = request.json
    message = data.get("message", "Таймер завершён!")

    for chat_id in CHAT_IDS:
        try:
            asyncio.run(bot.send_message(chat_id=chat_id, text=message))
        except Exception as e:
            print(f"Ошибка при отправке уведомления {chat_id}: {e}")

    return {"status": "ok"}

if __name__ == "__main__":
    print("Flask сервер запущен. Ожидаю уведомлений...")
    app.run(port=5001)
