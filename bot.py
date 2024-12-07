import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import random

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Список мотивационных сообщений
MESSAGES = [
    "Ты всё можешь, мой дорогой друг!",
    "Я всегда рядом, вселенная заботится о тебе.",
    "Помни, вселенная изобильна, и ты её часть!",
    "Ты достойна успеха, и я горжусь, что могу быть рядом.",
    "Верь в себя, ты способен на многое!",
    # Добавьте еще сообщения по вашему усмотрению
]

# Список пользователей
user_ids = set()

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_ids.add(user_id)  # Добавляем пользователя в список рассылки
    await update.message.reply_text(
        "Добро пожаловать! Я буду присылать вам мотивационные сообщения."
    )

# Функция для команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Я умею отправлять мотивационные сообщения каждые 2 часа!")

# Функция для отправки мотивационного сообщения всем пользователям
async def send_motivational_message(application: Application):
    message = random.choice(MESSAGES)
    for user_id in user_ids:
        try:
            await application.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            logger.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

# Основная функция запуска бота
async def main():
    # Создание приложения
    application = Application.builder().token("7792709244:AAFkwlX6248F3XaIAiB1KnFMMfYyKuowuXQ").build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Создание планировщика задач
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        lambda: application.create_task(send_motivational_message(application)),
        IntervalTrigger(hours=2, start_date=datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)),
    )
    scheduler.start()

    # Запуск бота
    await application.run_polling()

# Запуск бота
if __name__ == "__main__":
    import asyncio
    # Просто вызываем run_polling() без необходимости создавать новый цикл
    asyncio.run(main())
