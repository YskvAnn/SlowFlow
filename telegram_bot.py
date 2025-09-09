from flask import Flask, request
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8293900584:AAGnknhlDJzhXo8ZqjwPlZS9irtPBJUm1ZI"
bot = Bot(token=TOKEN)
app = Flask(__name__)

# Список пользователей, которым будут приходить уведомления
CHAT_IDS = set()  # используем set, чтобы не было повторов

# ---------- Telegram Bot для сбора chat_id ----------
async def start(update: ContextTypes.DEFAULT_TYPE, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    CHAT_IDS.add(chat_id)  # сохраняем нового пользователя
    await update.message.reply_text(f"Привет! Теперь ты будешь получать уведомления. Твой chat_id: {chat_id}")

# Запуск Telegram бота для /start
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

# Функция для отправки уведомлений всем пользователям
def send_notification(message):
    for chat_id in CHAT_IDS:
        bot.send_message(chat_id=chat_id, text=message)

# ---------- Flask сервер для получения сигналов от фронтенда ----------
@app.route("/notify", methods=["POST"])
def notify():
    data = request.json
    message = data.get("message", "Таймер завершён!")
    send_notification(message)
    return {"status": "ok"}

# ---------- Запуск Telegram бота и Flask сервера ----------
if __name__ == "__main__":
    import threading

    # Запускаем Telegram бота в отдельном потоке
    t = threading.Thread(target=application.run_polling, daemon=True)
    t.start()

    # Запускаем Flask сервер
    app.run(port=5000)
