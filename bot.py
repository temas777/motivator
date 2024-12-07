from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import random

# Ваш токен
TOKEN = "7792709244:AAFkwlX6248F3XaIAiB1KnFMMfYyKuowuXQ"

# Список мотивационных сообщений
messages = [
    "Ты всё можешь, мой дорогой друг!",
    "Я всегда рядом, вселенная заботится о тебе.",
    # Добавьте остальные сообщения
]

# Функция отправки мотивационных сообщений
async def send_message_to_users(context: ContextTypes.DEFAULT_TYPE):
    message = random.choice(messages)
    for chat_id in context.bot_data.get("user_chat_ids", []):
        try:
            await context.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    context.bot_data.setdefault("user_chat_ids", set()).add(chat_id)
    await update.message.reply_text("Добро пожаловать! Я буду отправлять тебе мотивационные сообщения.")

# Основная функция
def main():
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))

    # Планировщик задач
    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.add_job(
        send_message_to_users,
        "interval",
        hours=2,  # Интервал отправки сообщений
        start_date=datetime.now().replace(hour=8, minute=0, second=0, microsecond=0),
        end_date=datetime.now().replace(hour=22, minute=0, second=0, microsecond=0),
        kwargs={"context": application.bot_data},
    )
    scheduler.start()

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
