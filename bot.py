from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Создаем кнопку Web App с объектом WebAppInfo
    keyboard = [
        [InlineKeyboardButton("Открыть Web App", web_app=WebAppInfo(url="https://www.youtube.com/watch?v=jVKlZd5LMBs"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с кнопкой
    await update.message.reply_text("Нажми кнопку:", reply_markup=reply_markup)


app = ApplicationBuilder().token("8253449029:AAGVWHt8F1fk82jooUMmkKqU3LCh-AAmt3Y").build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
