import random
import time
import schedule
from datetime import datetime
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

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
        schedule.every(2).hours.do(send_random_message, context=chat_id)

# Основная функция для запуска бота
def main():
    updater = Updater("7792709244:AAFkwlX6248F3XaIAiB1KnFMMfYyKuowuXQ", use_context=True)
    dp = updater.dispatcher

    # Обработчики команд и сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, start))

    # Запуск планировщика с проверкой времени
    while True:
        if is_time_to_send():
            schedule.run_pending()  # Запускаем запланированные задачи
        time.sleep(60)  # Пауза в 1 минуту между проверками времени

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
