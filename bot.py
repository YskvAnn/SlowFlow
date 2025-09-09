from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Application
from telegram import Bot
import asyncio

TOKEN = "8293900584:AAGnknhlDJzhXo8ZqjwPlZS9irtPBJUm1ZI"

async def clear_updates():
    bot = Bot(TOKEN)
    updates = await bot.get_updates(offset=-1)
    if updates:
        print(f"Пропущено {len(updates)} старых апдейтов")
    else:
        print("Старых апдейтов нет")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Открыть Web App", web_app=WebAppInfo(url="https://yskvann.github.io/SlowFlow/"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Нажми кнопку:", reply_markup=reply_markup)

async def main():
    await clear_updates()
    app: Application = ApplicationBuilder().t
