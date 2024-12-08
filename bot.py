import logging
import random
from datetime import datetime, time
from telegram.ext import Application

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Укажите ваш chat_id
YOUR_CHAT_ID = 595754409  # Замените на ваш chat_id

# Укажите токен вашего бота
BOT_TOKEN = "7792709244:AAFkwlX6248F3XaIAiB1KnFMMfYyKuowuXQ"  # Замените на ваш токен

# Список сообщений
messages = [
    "Привет! Как дела?",
    "Не забывай делать перерывы!",
    "Ты молодец, так держать!",
    "Как твое настроение?",
    "Напоминаю, что всё будет хорошо!",
]

# Основная функция
async def send_random_message_and_exit():
    current_time = datetime.now().time()
    if time(8, 0) <= current_time <= time(22, 0):  # Проверяем временной диапазон
        message = random.choice(messages)
        application = Application.builder().token(BOT_TOKEN).build()
        await application.bot.send_message(chat_id=YOUR_CHAT_ID, text=message)
        logger.info(f"Отправлено сообщение: {message}")
    else:
        logger.info("Не время для отправки сообщения.")
    exit()  # Завершение работы скрипта

# Запуск
if __name__ == "__main__":
    import asyncio

    asyncio.run(send_random_message_and_exit())
