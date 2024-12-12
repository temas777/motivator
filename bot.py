import logging
import random
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка токена бота
with open("bot_token.txt", "r") as token_file:
    BOT_TOKEN = token_file.read().strip()

# Данные
DATA_PATH = "./data"
GENERAL_MESSAGES_FILE = os.path.join(DATA_PATH, "messages.txt")
MORNING_MESSAGES_FILE = os.path.join(DATA_PATH, "morning_messages.txt")
EVENING_MESSAGES_FILE = os.path.join(DATA_PATH, "evening_messages.txt")

# Создание приложения
application = Application.builder().token(BOT_TOKEN).build()

# Список пользователей
users = set()


def load_messages(file_path):
    """Функция загрузки сообщений из файла."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    return []


async def send_morning_message(context: CallbackContext):
    """Отправка утреннего сообщения."""
    messages = load_messages(MORNING_MESSAGES_FILE)
    if messages:
        message = random.choice(messages)
        for user_id in users:
            try:
                await context.bot.send_message(chat_id=user_id, text=message)
            except Exception as e:
                logger.error(f"Ошибка при отправке утреннего сообщения пользователю {user_id}: {e}")


async def send_evening_message(context: CallbackContext):
    """Отправка вечернего сообщения."""
    messages = load_messages(EVENING_MESSAGES_FILE)
    if messages:
        message = random.choice(messages)
        for user_id in users:
            try:
                await context.bot.send_message(chat_id=user_id, text=message)
            except Exception as e:
                logger.error(f"Ошибка при отправке вечернего сообщения пользователю {user_id}: {e}")


async def start(update: Update, context: CallbackContext):
    """Обработчик команды /start."""
    user_id = update.effective_user.id
    if user_id not in users:
        users.add(user_id)
        await update.message.reply_text("Вы подписаны на уведомления!")
        logger.info(f"Новый пользователь: {user_id}")
    else:
        await update.message.reply_text("Вы уже подписаны.")


def add_schedulers(application):
    """Добавление задач в планировщик."""
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
    scheduler.start()
    logger.info("Планировщик запущен.")


async def delete_existing_webhook():
    """Удаление существующего вебхука перед запуском polling."""
    try:
        await application.bot.delete_webhook()
        logger.info("Вебхук успешно удалён.")
    except Exception as e:
        logger.error(f"Ошибка при удалении вебхука: {e}")


if __name__ == "__main__":
    # Удаляем вебхук перед запуском polling
    application.post_init = delete_existing_webhook

    # Добавление обработчиков
    application.add_handler(CommandHandler("start", start))

    # Добавление задач планировщика
    add_schedulers(application)

    # Запуск бота
    logger.info("Бот запущен.")
    application.run_polling()
