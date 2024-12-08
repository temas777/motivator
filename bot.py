import random
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, CallbackContext
from telegram.ext import filters
import logging

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Список случайных сообщений
messages = [
    "Привет! Как дела?",
    "Что нового?",
    "Как твои успехи?",
    "У тебя все хорошо?",
    "Привет! Чем занимаешься?"
]

# Функция для обработки текстовых сообщений
async def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    await update.message.reply_text("Привет! Я буду отправлять тебе случайные сообщения.")
    logger.info(f"Бот начал общение с пользователем {chat_id}")

# Функция для отправки случайного сообщения
def send_random_message(context: CallbackContext):
    chat_id = context.job.context
    message = random.choice(messages)
    context.bot.send_message(chat_id=chat_id, text=message)
    logger.info(f"Отправлено сообщение: {message} в чат {chat_id}")

# Основная функция для запуска бота
def main():
    # Создание приложения
    application = Application.builder().token("7792709244:AAFkwlX6248F3XaIAiB1KnFMMfYyKuowuXQ").build()

    # Регистрация обработчика текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))

    # Планировщик задач
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_random_message, 'interval', hours=2, context="CHAT_ID")  # Укажите корректный CHAT_ID
    scheduler.start()

    # Запуск бота
    logger.info("Бот запущен и работает")
    application.run_polling()

if __name__ == '__main__':
    main()
