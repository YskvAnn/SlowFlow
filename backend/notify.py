from flask import Flask, request
from telegram import Bot
import asyncio

TOKEN = "твой_токен"
bot = Bot(token=TOKEN)
CHAT_IDS = set()

app = Flask(__name__)

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
    app.run(port=5001)
