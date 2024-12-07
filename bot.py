from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import random

# Список мотивационных сообщений
messages = [
    "Ты всё можешь, мой дорогой друг!",
    "Я всегда рядом, вселенная заботится о тебе.",
    "Помни, вселенная изобильна, и ты её часть!",
    "Ты достойна успеха, и я горжусь, что могу быть рядом.",
    "Верь в себя, ты способен на многое!",
    # добавьте остальные сообщения...
]

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привет! Я бот, который будет мотивировать тебя!")

def send_motivation(update: Update, context: CallbackContext) -> None:
    message = random.choice(messages)
    update.message.reply_text(message)

def main():
    updater = Updater("7792709244:AAFkwlX6248F3XaIAiB1KnFMMfYyKuowuXQ")

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    # Запуск планировщика для регулярной рассылки сообщений
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_motivation, IntervalTrigger(hours=2, start_date='2024-01-01 08:00:00', end_date='2024-01-01 22:00:00'), args=[update, context])
    scheduler.start()

    updater.start_polling()

if __name__ == '__main__':
    main()
