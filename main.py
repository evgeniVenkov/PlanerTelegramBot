import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
from GptClient import GPTClient

# Загружаем токен из .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Логирование (чтобы видеть ошибки и события)
logging.basicConfig(level=logging.INFO)

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

gpt_client = GPTClient()

# Команда /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("👋 Привет! Я бот-планировщик. Используй /help, чтобы узнать команды.")
# Обработчик команды /start

# Команда /help
@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer("📌 Список команд:\n"
                         "/start - Запустить бота\n"
                         "/help - Список команд\n"
                         "/add_task - Добавить задачу\n"
                         "/edit_task - Изменить задачу")


from datetime import datetime


@dp.message()
async def echo_message(message: Message):

    message_time = message.date.strftime("%Y-%m-%d %H:%M:%S")  # нужный формат
    promt = f"{message.from_user.username} | {message_time} | {message.text} "

    print(f"📩 Новое сообщение от {promt} ")

    response = gpt_client.chat(promt)

    await message.answer(response)


# Запуск бота

# Обработчик всех текстовых сообщений

# Запуск бота
async def main():
    print("✅ Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
