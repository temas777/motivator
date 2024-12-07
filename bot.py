import random
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram.ext import filters  # Новый способ импорта filters

# Список сообщений
messages = [
    "Привет! Как дела?",
    "Что нового?",
    "Как твои успехи?",
    "У тебя все хорошо?",
    "Привет! Чем занимаешься?"
]

# Функция для отправки рандомного сообщения
def send_random_message(context: CallbackContext):
    chat_id = context.job.context
    message = random.choice(messages)
    context.bot.send_message(chat_id=chat_id, text=message)

# Функция для проверки времени (с 8 до 22)
def is_time_to_send():
    current_hour = datetime.now().hour
    return 8 <= current_hour < 22

# Функция для обработки новых сообщений
def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    update.message.reply_text("Привет! Я буду отправлять тебе случайные сообщения.")
    
    # Запланировать отправку сообщений, только если сейчас время для этого
    if is_time_to_send():
        # Создание и запуск планировщика
        scheduler = BackgroundScheduler()
        scheduler.add_job(send_random_message, 'interval', hours=2, start_date='2024-12-08 08:00:00', context=chat_id)
        scheduler.start()

# Основная функция для запуска бота
def main():
    updater = Updater("7792709244:AAFkwlX6248F3XaIAiB1KnFMMfYyKuowuXQ", use_context=True)
    dp = updater.dispatcher

    # Обработчики команд и сообщений
    dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))  # Обновленный фильтр

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
