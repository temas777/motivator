import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import random

# Список мотивационных сообщений
messages = [
    "Ты всё можешь, мой дорогой друг!",
    "Я всегда рядом, вселенная заботится о тебе.",
    "Помни, вселенная изобильна, и ты её часть!",
    # Добавьте еще 47 сообщений
]

# Список пользователей
users = []

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    if user_id not in users:
        users.append(user_id)
    await update.message.reply_text("Привет! Я твой мотивационный бот. Готов вдохновлять тебя каждый день!")

# Функция для отправки сообщений всем пользователям
async def send_motivational_message(application: Application):
    message = random.choice(messages)
    for user_id in users:
        try:
            await application.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            print(f"Ошибка отправки сообщения пользователю {user_id}: {e}")

# Настройка и запуск приложения
async def main():
    # Создаем приложение
    application = Application.builder().token("7792709244:AAFkwlX6248F3XaIAiB1KnFMMfYyKuowuXQ").build()

    # Регистрация команды /start
    application.add_handler(CommandHandler("start", start))

    # Планировщик
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        lambda: application.create_task(send_motivational_message(application)),
        IntervalTrigger(hours=2, start_date="2024-12-08 08:00:00", end_date="2024-12-08 22:00:00")
    )
    scheduler.start()

    # Запуск бота
    await application.run_polling()

# Проверяем активен ли цикл событий и запускаем код
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Если цикл уже активен, создаем задачу
            loop.create_task(main())
        else:
            # Если цикла нет, запускаем его
            asyncio.run(main())
    except Exception as e:
        print(f"Ошибка запуска бота: {e}")
