import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
from triger import Pauk
import pandas as pd
from Data_base import command

# Загружаем токен из .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Логирование (чтобы видеть ошибки и события)
logging.basicConfig(level=logging.INFO)

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()


# Команда /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("👋 Привет! Я бот-планировщик. Используй /help, чтобы узнать команды.\n"
                         "лучше всего начинать наш диалог с приветствия но можешь и просто написать задачу.")
# Обработчик команды /start

# Команда /help
@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer("📌 Список команд:\n"
                         "/start - Запустить бота\n"
                         "/help - Список команд\n"
                         )


from datetime import datetime


@dp.message()
async def echo_message(message: Message):

    message_time = message.date.strftime("%Y-%m-%d %H:%M:%S")  # нужный формат
    promt = f"{message.text}|{message_time}"

    print(f"📩 {promt} ")

    result_trigger = Pauk(message.text)

    if result_trigger is not None:
        result = command(result_trigger[0],promt)
        if isinstance(result, pd.DataFrame):
            result = result.to_string()

    else:
        result = "простите ваша команда не распознана"


    await message.answer(result)


# Запуск бота

# Обработчик всех текстовых сообщений

# Запуск бота
async def main():
    print("✅ Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
