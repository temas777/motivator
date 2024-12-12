import logging
import random
from telegram import Update, InputMediaPhoto, InputMediaVideo
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import time, datetime
import os

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка токена бота
with open("bot_token.txt", "r") as token_file:
    BOT_TOKEN = token_file.read().strip()

# Групповой chat_id
GROUP_CHAT_ID = -1001234567890  # Замените на ваш chat_id группы

# Данные
DATA_PATH = "./data"
GENERAL_MESSAGES_FILE = os.path.join(DATA_PATH, "messages.txt")
MORNING_MESSAGES_FILE = os.path.join(DATA_PATH, "morning_messages.txt")
EVENING_MESSAGES_FILE = os.path.join(DATA_PATH, "evening_messages.txt")
MEDIA_PATH = os.path.join(DATA_PATH, "media")

# Создание приложения
application = Application.builder().token(BOT_TOKEN).build()

# Список пользователей
users = set()

# Функция для загрузки текстовых сообщений
def load_messages(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    return []

# Утреннее сообщение
async def send_morning_message(context: CallbackContext):
    messages = load_messages(MORNING_MESSAGES_FILE)
    if messages:
        message = random.choice(messages)
        for user_id in users:
            await context.bot.send_message(chat_id=user_id, text=message)
        logger.info("Утреннее сообщение отправлено.")
    else:
        logger.warning("Нет утренних сообщений для отправки.")

# Вечернее сообщение
async def send_evening_message(context: CallbackContext):
    messages = load_messages(EVENING_MESSAGES_FILE)
    if messages:
        message = random.choice(messages)
        for user_id in users:
            await context.bot.send_message(chat_id=user_id, text=message)
        logger.info("Вечернее сообщение отправлено.")
    else:
        logger.warning("Нет вечерних сообщений для отправки.")

# Перенаправление ответов в группу
async def handle_response(update: Update, context: CallbackContext):
    if update.message.reply_to_message:  # Проверяем, что это ответ
        reply_text = update.message.text
        await context.bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=f"Ответ от {update.effective_user.first_name}: {reply_text}",
        )
        logger.info("Ответ перенаправлен в группу.")

# Отправка общего сообщения
async def send_general_message(context: CallbackContext):
    messages = load_messages(GENERAL_MESSAGES_FILE)
    if messages:
        message = random.choice(messages)
        for user_id in users:
            await context.bot.send_message(chat_id=user_id, text=message)
        logger.info("Общее сообщение отправлено.")
    else:
        logger.warning("Нет сообщений для отправки.")

# Команда /start
async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in users:
        users.add(user_id)
        await update.message.reply_text("Вы успешно подписаны на мотивационные сообщения!")
        logger.info(f"Новый пользователь добавлен: {user_id}")
    else:
        await update.message.reply_text("Вы уже подписаны!")

# Добавление планировщика
def add_schedulers(application):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_morning_message,
        "cron",
        hour=8,
        minute=0,
        args=[application],
    )
    scheduler.add_job(
        send_evening_message,
        "cron",
        hour=21,
        minute=0,
        args=[application],
    )
    scheduler.add_job(
        send_general_message,
        "interval",
        hours=2,
        args=[application],
    )
    scheduler.start()
    logger.info("Планировщик запущен.")

# Основной запуск бота
if __name__ == "__main__":
    # Добавление обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.REPLY, handle_response))

    # Добавление планировщика
    add_schedulers(application)

    logger.info("Бот запущен.")
    application.run_polling()
