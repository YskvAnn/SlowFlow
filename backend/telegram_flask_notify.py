from flask import Flask, request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

TOKEN = "ВАШ_ТОКЕН_БОТА"
bot = Bot(token=TOKEN)
app = Flask(__name__)

# Разрешаем CORS для теста
from flask_cors import CORS
CORS(app)

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

# ---------- Flask endpoint ----------
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

if __name__ == "__main__":
    print("Flask сервер запущен на 5001. Жду уведомлений...")
    print("Бот запущен. Жду /start...")
    application.run_polling()
