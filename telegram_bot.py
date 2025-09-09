# telegram_bot.py
from flask import Flask, request
from telegram import Bot

# Вставь сюда токен твоего бота
TOKEN = "ТВОЙ_ТОКЕН"
# Вставь сюда свой chat_id (можно узнать через @userinfobot)
CHAT_ID = "ТВОЙ_CHAT_ID"

bot = Bot(token=TOKEN)
app = Flask(__name__)

@app.route("/notify", methods=["POST"])
def notify():
    data = request.json
    message = data.get("message", "Таймер завершён!")
    bot.send_message(chat_id=CHAT_ID, text=message)
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(port=5000)
