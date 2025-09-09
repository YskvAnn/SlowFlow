from flask import Flask, request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import threading
import asyncio

TOKEN = "8293900584:AAGnknhlDJzhXo8ZqjwPlZS9irtPBJUm1ZI"
bot = Bot(token=TOKEN)
app = Flask(__name__)

CHAT_IDS = set()

# ---------- Telegram Bot ----------
async def start(update: ContextTypes.DEFAULT_TYPE, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    CHAT_IDS.add(chat_id)

    keyboard = [[InlineKeyboardButton(
        "Открыть апку",
        web_app=WebAppInfo(url="https://yskvann.github.io/SlowFlow/")
    )]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Запусти таймер через апку:", reply_markup=reply_markup)

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

# ---------- Flask ----------
@app.route("/notify", methods=["POST"])
def notify():
    data = request.json
    message = data.get("message", "Таймер завершён!")
    for chat_id in CHAT_IDS:
        try:
            # создаем отдельный цикл для асинхронной функции
            asyncio.run(bot.send_message(chat_id=chat_id, text=message))
        except Exception as e:
            print(f"Ошибка при отправке уведомления {chat_id}: {e}")
    return {"status": "ok"}

if __name__ == "__main__":
    # Запускаем Flask в отдельном потоке
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5001), daemon=True).start()
    print("Flask сервер запущен. Ожидаю уведомлений...")

    # Запускаем Telegram бота в основном потоке
    print("Бот запущен. Жду /start...")
    application.run_polling()
