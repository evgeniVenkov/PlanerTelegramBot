import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
from triger import Pauk
import pandas as pd
from Data_base import command_add,command_search
from client import client
from promt import get_сhat

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


def request_processing(result_trigger, promt, username):

    if result_trigger == "add":
        result = command_add(promt,username)
        if isinstance(result, pd.DataFrame):
            print(f"((main){result}")
            if result.shape[0] < 2:
                result = result.squeeze()
                result = (f"Данная дата: {str(result["date"])}\n "
                          f"время: {str(result["time"])}\n"
                          f"заняты задачей: {str(result["task"])}")
    elif result_trigger == "search":
        result = command_search(promt, username)
        result = result.to_string()
    else:
        result =f"(main)\n{result_trigger}"
        print(result_trigger)

    return result


@dp.message()
async def echo_message(message: Message):

    message_time = message.date.strftime("%Y-%m-%d %H:%M:%S")  # нужный формат
    promt = f"{message.text}|{message_time}"

    print(f"📩 {promt} ")

    result_trigger = Pauk(message.text)

    if result_trigger is not None:
        result = request_processing(result_trigger,promt,message.from_user.username)


    else:
        print("None")
        gpt = client(get_сhat())
        result = gpt.chat(promt)

    await message.answer(result)


# Запуск бота

# Обработчик всех текстовых сообщений

# Запуск бота
async def main():
    print("✅ Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
