from flask import Flask, request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import threading

TOKEN = "8293900584:AAGnknhlDJzhXo8ZqjwPlZS9irtPBJUm1ZI"
bot = Bot(token=TOKEN)
app = Flask(__name__)

# Разрешаем CORS (для теста и Web App)
from flask_cors import CORS
CORS(app)

CHAT_IDS = set()

# ---------- Telegram Bot ----------
async def start(update: ContextTypes.DEFAULT_TYPE, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    CHAT_IDS.add(chat_id)

    keyboard = [[InlineKeyboardButton(
        "Открыть апку",
        web_app=WebAppInfo(url="https://yskvann.github.io/SlowFlow/")  # ссылка на твою апку
    )]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Запусти таймер через апку:", reply_markup=reply_markup)

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

# ---------- Flask endpoint для уведомлений ----------
@app.route("/notify", methods=["POST"])
def notify():
    data = request.json
    message = data.get("message", "Таймер завершён!")

    async def send_all():
        for chat_id in CHAT_IDS:
            try:
                await bot.send_message(chat_id=chat_id, text=message)
            except Exception as e:
                print(f"Ошибка уведомления {chat_id}: {e}")

    # Запускаем асинхронно
    asyncio.create_task(send_all())
    return {"status": "ok"}

# ---------- Запуск Flask и Telegram ----------
if __name__ == "__main__":
    # Функция для запуска Flask
    def run_flask():
        print("Flask сервер запущен на 5001. Жду уведомлений...")
        app.run(host="0.0.0.0", port=5001)

    # Запускаем Flask в отдельном потоке
    threading.Thread(target=run_flask).start()

    # Запускаем Telegram бота
    print("Бот запущен. Жду /start...")
    application.run_polling()
