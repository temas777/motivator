import logging
import random
from datetime import datetime, time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.ext import Application, CommandHandler

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Укажите токен вашего бота
BOT_TOKEN = "7792709244:AAFkwlX6248F3XaIAiB1KnFMMfYyKuowuXQ"  # Замените на ваш токен

# Список сообщений
messages = [
    "Ты легко достигаешь успеха!",
    "Деньги любят тебя!",
    "Ты легко привлекаешь деньги в свою жизнь!",
    "У тебя всегда достаточно ресурсов для счастья!",
    "Ты сохраняешь спокойствие в любой ситуации!",
    "Ты находишь гармонию между работой и отдыхом!",
    "Ты живёшь так, как всегда мечтал!",
]

# Хранилище chat_id пользователей
user_chat_ids = set()

# Обработчик команды /start
async def start(update, context):
    chat_id = update.effective_chat.id
    user_chat_ids.add(chat_id)  # Добавляем chat_id в список
    await context.bot.send_message(chat_id=chat_id, text="Привет! Теперь я буду присылать тебе сообщения каждые 2 часа.")

# Функция для отправки сообщения
async def send_random_message(application: Application):
    current_time = datetime.now().time()
    if time(8, 0) <= current_time <= time(22, 0):  # Проверяем временной диапазон
        for chat_id in user_chat_ids:
            message = random.choice(messages)
            try:
                await application.bot.send_message(chat_id=chat_id, text=message)
                logger.info(f"Отправлено сообщение пользователю {chat_id}: {message}")
            except Exception as e:
                logger.error(f"Ошибка при отправке сообщения пользователю {chat_id}: {e}")
    else:
        logger.info("Не время для отправки сообщений.")

# Основная функция
def main():
    # Создаём приложение Telegram Bot API
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))

    # Создаём планировщик
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_random_message, "interval", hours=1, args=[application])

    # Запускаем планировщик
    scheduler.start()
    logger.info("Планировщик запущен.")

    # Запуск бота
    application.run_polling()

# Запуск
if __name__ == "__main__":
    main()
