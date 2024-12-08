import logging
import random
from datetime import datetime, time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN  # Импорт токена из config.py

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Список сообщений
messages = [
    "Ты можешь всё!",
    "Сегодня твой день!",
    "Двигайся вперёд, несмотря на всё!",
    "Ты способен достичь любых целей!",
    "Сделай шаг к своей мечте уже сегодня!",
    "Никогда не сдавайся!",
    "У тебя всё получится!",
]

# Список пользователей
user_chat_ids = set()

# Команда /start
async def start(update, context):
    chat_id = update.effective_chat.id
    if chat_id not in user_chat_ids:
        user_chat_ids.add(chat_id)
        logger.info(f"Добавлен новый пользователь: {chat_id}")
    await update.message.reply_text(
        "Привет! Теперь ты будешь получать мотивационные сообщения каждые 3 часа с 8 утра до 10 вечера."
    )

# Функция для отправки сообщений
async def send_random_message(application):
    current_time = datetime.now().time()
    if time(8, 0) <= current_time <= time(22, 0):
        for chat_id in user_chat_ids:
            try:
                message = random.choice(messages)
                await application.bot.send_message(chat_id=chat_id, text=message)
                logger.info(f"Отправлено сообщение пользователю {chat_id}: {message}")
            except Exception as e:
                logger.error(f"Ошибка отправки сообщения пользователю {chat_id}: {e}")
    else:
        logger.info("Бот спит. Не время для отправки сообщений.")

# Основная функция
def main():
    # Создание приложения Telegram
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавление обработчиков
    application.add_handler(CommandHandler("start", start))

    # Планировщик задач
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_random_message, "interval", hours=3, args=[application])
    scheduler.start()

    # Запуск бота
    logger.info("Бот запущен.")
    application.run_polling()

if __name__ == "__main__":
    main()
