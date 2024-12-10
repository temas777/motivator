import logging
import random
from datetime import datetime, time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram import Update, InputMediaPhoto, InputMediaVideo
from config import BOT_TOKEN, GROUP_CHAT_ID

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Списки для хранения данных
user_chat_ids = set()  # Пользователи, запустившие бота
messages = ["Ты можешь всё!", "Сегодня твой день!", "Никогда не сдавайся!"]
daily_morning_messages = ["Доброе утро! Что вы сегодня планируете сделать?"]
daily_evening_messages = ["Как прошел ваш день? Что удалось достичь?"]
media_files = []  # Список для хранения медиафайлов (фото/видео)

# Интервал отправки сообщений (по умолчанию 3 часа)
message_interval = 3

# Команда /start
async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id not in user_chat_ids:
        user_chat_ids.add(chat_id)
        logger.info(f"Добавлен новый пользователь: {chat_id}")
    await update.message.reply_text(
        "Привет! Теперь вы будете получать мотивационные сообщения.\n"
        "Используйте /set_interval <число часов>, чтобы изменить интервал.\n"
        "Используйте /add_messages <текст> для добавления новых сообщений.\n"
        "Вы также можете отправлять фото/видео для добавления в список отправки."
    )

# Команда для изменения интервала
async def set_interval(update: Update, context: CallbackContext):
    global message_interval
    try:
        interval = int(context.args[0])
        if interval > 0:
            message_interval = interval
            await update.message.reply_text(f"Интервал установлен на {message_interval} часов.")
        else:
            await update.message.reply_text("Интервал должен быть больше 0.")
    except (IndexError, ValueError):
        await update.message.reply_text("Пожалуйста, укажите число часов: /set_interval <число часов>.")

# Команда для добавления текстовых сообщений
async def add_messages(update: Update, context: CallbackContext):
    new_messages = " ".join(context.args).split(",")
    messages.extend([msg.strip() for msg in new_messages if msg.strip()])
    await update.message.reply_text(f"Добавлены новые сообщения: {', '.join(new_messages)}")

# Обработчик медиафайлов
async def handle_media(update: Update, context: CallbackContext):
    media = update.message.photo or update.message.video
    if media:
        file_id = media[-1].file_id  # Берем файл с наивысшим качеством
        media_files.append(file_id)
        await update.message.reply_text("Файл добавлен в список отправки!")

# Отправка рандомного сообщения
async def send_random_message(application):
    current_time = datetime.now().time()
    if time(8, 0) <= current_time <= time(22, 0):
        for chat_id in user_chat_ids:
            content = random.choice(messages + media_files)
            if content.startswith("http"):  # Если это файл (фото/видео)
                if content in media_files:
                    media = InputMediaPhoto(media=content) if content.endswith("photo") else InputMediaVideo(media=content)
                    await application.bot.send_media_group(chat_id=chat_id, media=[media])
            else:  # Если это текст
                await application.bot.send_message(chat_id=chat_id, text=content)
    else:
        logger.info("Бот спит. Не время для отправки сообщений.")

# Утреннее сообщение
async def send_morning_message(application):
    content = random.choice(daily_morning_messages)
    for chat_id in user_chat_ids:
        await application.bot.send_message(chat_id=chat_id, text=content)

# Вечернее сообщение
async def send_evening_message(application):
    content = random.choice(daily_evening_messages)
    for chat_id in user_chat_ids:
        await application.bot.send_message(chat_id=chat_id, text=content)

# Ответы в группу
async def forward_to_group(update: Update, context: CallbackContext):
    text = update.message.text
    if update.effective_chat.id in user_chat_ids:
        await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=f"Ответ от {update.effective_user.first_name}: {text}")

# Основная функция
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set_interval", set_interval))
    application.add_handler(CommandHandler("add_messages", add_messages))

    # Обработчики сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_group))
    application.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, handle_media))

    # Планировщик задач
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_random_message, "interval", hours=message_interval, args=[application])
    scheduler.add_job(send_morning_message, "cron", hour=8, args=[application])
    scheduler.add_job(send_evening_message, "cron", hour=21, args=[application])
    scheduler.start()

    logger.info("Бот запущен.")
    application.run_polling()

if __name__ == "__main__":
    main()
