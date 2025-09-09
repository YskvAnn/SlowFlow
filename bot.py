from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8293900584:AAGnknhlDJzhXo8ZqjwPlZS9irtPBJUm1ZI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return  # Защита на случай группы
    keyboard = [
        [InlineKeyboardButton("Открыть Web App", web_app=WebAppInfo(url="https://yskvann.github.io/SlowFlow/"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Нажми кнопку:", reply_markup=reply_markup)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
