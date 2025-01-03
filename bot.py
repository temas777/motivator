import logging
import random
import os
from datetime import time
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка токена бота
with open("bot_token.txt", "r") as token_file:
    BOT_TOKEN = token_file.read().strip()

# Групповой chat_id
GROUP_CHAT_ID = -4651813337  # Замените на ваш chat_id группы

# Пути к данным
DATA_PATH = "./data"
GENERAL_MESSAGES_FILE = os.path.join(DATA_PATH, "messages.txt")
MORNING_MESSAGES_FILE = os.path.join(DATA_PATH, "morning_messages.txt")
EVENING_MESSAGES_FILE = os.path.join(DATA_PATH, "evening_messages.txt")

# Список пользователей
users = set()

# Создание приложения
application = Application.builder().token(BOT_TOKEN).build()

# Функция для загрузки текстовых сообщений
def load_messages(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    return []

# Отправка сообщений с проверкой
async def send_message_with_check(context: CallbackContext, message, user_id):
    try:
        await context.bot.send_message(chat_id=user_id, text=message)
        logger.info(f"Сообщение успешно отправлено пользователю {user_id}.")
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения пользователю {user_id}: {e}")

# Утреннее сообщение
async def send_morning_message(context: CallbackContext):
    messages = load_messages(MORNING_MESSAGES_FILE)
    if messages:
        message = random.choice(messages)
        await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=message)
        logger.info("Утреннее сообщение отправлено в группу.")
    else:
        logger.warning("Нет утренних сообщений для отправки.")

# Вечернее сообщение
async def send_evening_message(context: CallbackContext):
    messages = load_messages(EVENING_MESSAGES_FILE)
    if messages:
        message = random.choice(messages)
        await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=message)
        logger.info("Вечернее сообщение отправлено в группу.")
    else:
        logger.warning("Нет вечерних сообщений для отправки.")

# Перенаправление ответов в группу
async def handle_response(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
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
            await send_message_with_check(context, message, user_id)
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

# Тестирование утреннего сообщения
async def test_morning_message(update: Update, context: CallbackContext):
    messages = load_messages(MORNING_MESSAGES_FILE)
    if messages:
        message = random.choice(messages)
        await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=f"[ТЕСТ] {message}")
        logger.info("Тестовое утреннее сообщение отправлено в группу.")
        await update.message.reply_text("Тестовое утреннее сообщение отправлено.")
    else:
        await update.message.reply_text("Нет утренних сообщений для теста.")
        logger.warning("Нет утренних сообщений для теста.")

# Тестирование вечернего сообщения
async def test_evening_message(update: Update, context: CallbackContext):
    messages = load_messages(EVENING_MESSAGES_FILE)
    if messages:
        message = random.choice(messages)
        await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=f"[ТЕСТ] {message}")
        logger.info("Тестовое вечернее сообщение отправлено в группу.")
        await update.message.reply_text("Тестовое вечернее сообщение отправлено.")
    else:
        await update.message.reply_text("Нет вечерних сообщений для теста.")
        logger.warning("Нет вечерних сообщений для теста.")

# Функция для удаления вебхуков
async def delete_existing_webhook(application):
    try:
        await application.bot.delete_webhook()
        logger.info("Вебхук успешно удалён.")
    except Exception as e:
        logger.error(f"Ошибка при удалении вебхука: {e}")

# Добавление задач в планировщик
def add_schedulers(application):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_morning_message,
        "cron",
        hour=6,
        minute=0,
        args=[application],
    )
    scheduler.add_job(
        send_evening_message,
        "cron",
        hour=19,
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
    # Удаление вебхука перед запуском polling
    application.post_init = lambda app: delete_existing_webhook(app)

    # Добавление обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("test_morning", test_morning_message))
    application.add_handler(CommandHandler("test_evening", test_evening_message))
    application.add_handler(MessageHandler(filters.REPLY, handle_response))

    # Добавление задач планировщика
    add_schedulers(application)

    # Запуск бота
    logger.info("Бот запущен.")
    application.run_polling()
