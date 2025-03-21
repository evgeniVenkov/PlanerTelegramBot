import os
import logging
import asyncio
from aiogram import Bot, Dispatcher,Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
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
router = Router()



# Обработчик кнопки "Редактировать"
@router.callback_query(F.data.startswith("edit_"))
async def edit_task(callback: CallbackQuery):
    task_name = callback.data.split("_", 1)[1]  # Получаем название задачи
    await callback.message.answer(f"✏️ Вы выбрали редактирование задачи: {task_name}")
    await callback.answer()  # Подтверждаем, что запрос был обработан

# Обработчик кнопки "Удалить"
@router.callback_query(F.data.startswith("delete_"))
async def delete_task(callback: CallbackQuery):
    task_name = callback.data.split("_", 1)[1]  # Получаем название задачи
    await callback.message.delete()  # Удаляем сообщение с задачей
    await callback.message.answer(f"🗑 Задача '{task_name}' удалена!")
    await callback.answer()  # Подтверждаем, что запрос был обработан

@router.callback_query(F.data.startswith("complite_"))
async def delete_task(callback: CallbackQuery):
    task_name = callback.data.split("_", 1)[1]  # Получаем название задачи
    await callback.message.delete()  # Удаляем сообщение с задачей
    await callback.message.answer(f"🗑 Задача '{task_name}' Выполнена!=!")
    await callback.answer()  # Подтверждаем, что запрос был обработан

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
    elif result_trigger == "search":
        result = command_search(promt, username)
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
        if isinstance(result, pd.DataFrame):
            for _, row in result.iterrows():
                task_name = row["task"]
                task_time = row["time"]

                # Создаём билдера для клавиатуры
                builder = InlineKeyboardBuilder()

                # Добавляем кнопки
                builder.button(
                    text="✏️ Редактировать",
                    callback_data=f"edit_{row['task']}"
                )
                builder.button(
                    text="🗑 Удалить",
                    callback_data=f"delete_{row['task']}"
                )
                builder.button(
                    text="👍 выполнена!",
                    callback_data=f"complite_{row['task']}"
                )

                # Создаём InlineKeyboardMarkup из билдера
                inline_keyboard = builder.as_markup()

                # Отправляем сообщение с кнопками
                await message.answer(
                    f"📝 {task_name} ⏰ Время: {task_time}",
                    reply_markup=inline_keyboard
                )
        else:
            await message.answer(result)

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

dp.include_router(router)

if __name__ == "__main__":
    asyncio.run(main())
