# backend/bot.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8293900584:AAGnknhlDJzhXo8ZqjwPlZS9irtPBJUm1ZI"
CHAT_IDS = set()  # сюда будут добавляться пользователи

# ---------- Обработчик /start ----------
async def start(update: ContextTypes.DEFAULT_TYPE, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    CHAT_IDS.add(chat_id)

    keyboard = [
        [InlineKeyboardButton(
            "Открыть Pomodoro",
            web_app=WebAppInfo(url="https://yskvann.github.io/SlowFlow/")
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Привет! Ты будешь получать уведомления. Твой chat_id: {chat_id}",
        reply_markup=reply_markup
    )

# ---------- Запуск бота ----------
if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    print("Бот запущен. Жду /start...")
    application.run_polling()
