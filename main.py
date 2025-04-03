import os
import logging
import asyncio
from aiogram import Bot, Dispatcher,Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv
from triger import Pauk
import pandas as pd
from Data_base import get_task,command_search,command_delete,command_update_id
from client import client
from promt import get_сhat,get_status_command
from aiogram.fsm.storage.memory import MemoryStorage





# Загружаем токен из .env
load_dotenv()
TOKEN = os.getenv("TOKEN")


# Логирование (чтобы видеть ошибки и события)
logging.basicConfig(level=logging.INFO)

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)

# Создаём хранилище
storage = MemoryStorage()

# Создаём диспетчер и маршрутизатор
dp = Dispatcher(storage=storage)
router = Router()

# Подключаем маршруты к диспетчеру
dp.include_router(router)
# Определяем состояния
class EditTaskState(StatesGroup):
    waiting_for_new_task = State()


@router.callback_query(F.data.startswith("edit_"))
async def edit_task(callback: CallbackQuery, state: FSMContext):
    data_parts = callback.data.split("_")
    if len(data_parts) < 3:
        await callback.message.answer("Ошибка: некорректный формат данных.")
        return

    task_id = data_parts[1]  # Получаем ID задачи
    task_name = "_".join(data_parts[2:])  # На случай, если в названии есть подчеркивания

    await state.update_data(task_id=task_id)  # Сохраняем ID задачи
    await callback.message.answer(f"✏️ Введите новый текст для задачи: {task_name}")
    await state.set_state(EditTaskState.waiting_for_new_task)  # Устанавливаем состояние ожидания ввода

    current_state = await state.get_state()
    print(f"Текущее состояние: {current_state}")

    await callback.answer()  # Подтверждаем обработку
@router.message(EditTaskState.waiting_for_new_task)
async def process_new_task(message: Message, state: FSMContext):
    new_task = message.text.strip()  # Убираем лишние пробелы
    data = await state.get_data()
    print("Simple text")
    task_id = data.get("task_id")  # Получаем ID задачи из состояния

    if not task_id:
        await message.answer("Ошибка: не удалось получить ID задачи.")
        await state.clear()
        return

    command_update_id(task_id, new_task)  # Обновляем задачу в БД или другом хранилище

    await message.answer(f"✅ Задача обновлена: {new_task}")
    await state.clear()  # Сбрасываем состояние
# Обработчик кнопки "Удалить"
@router.callback_query(F.data.startswith("delete_"))
async def delete_task(callback: CallbackQuery):
    task_name = callback.data.split("_" )[2]
    id = callback.data.split("_")[1]
    command_delete(id)

    await callback.message.delete()  # Удаляем сообщение с задачей
    await callback.message.answer(f"🗑 Задача {task_name}")
    await callback.answer()  # Подтверждаем, что запрос был обработан
@router.callback_query(F.data.startswith("complite_"))
async def complite_task(callback: CallbackQuery):
    task_name = callback.data.split("_")[2]  # Получаем название задачи
    await callback.message.delete()  # Удаляем сообщение с задачей
    await callback.message.answer(f"👍Задача '{task_name}' Выполнена!=!")
    await callback.answer()  # Подтверждаем, что запрос был обработан
# Команда /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("👋 Привет! Я бот-планировщик. Используй /help, чтобы узнать команды.\n"
                         "лучше всего начинать наш диалог с приветствия но можешь и просто написать задачу.")
# Команда /help
@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer("📌 Список команд:\n"
                         "/start - Запустить бота\n"
                         "/help - Список команд\n"
                         )
def request_processing(result_trigger, promt, username):

    if result_trigger == "add":
        result = get_task(promt, username)
    elif result_trigger == "search":
        result = command_search(promt, username)
    else:
        result =f"(main)\n{result_trigger}"
        print(result_trigger)

    return result
def get_inliner(row):
    # Создаём билдера для клавиатуры
    builder = InlineKeyboardBuilder()

    # Добавляем кнопки
    builder.button(
        text="✏️ Редактировать",
        callback_data=f"edit_{row['id']}_{row['task']}"
    )
    builder.button(
        text="🗑 Удалить",
        callback_data=f"delete_{row['id']}_{row['task']}"
    )
    builder.button(
        text="👍 выполнена!",
        callback_data=f"complite_{row['id']}_{row['task']}"
    )

    # Создаём InlineKeyboardMarkup из билдера
    return builder.as_markup()
@dp.message()
async def echo_message(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == EditTaskState.waiting_for_new_task.state:
        await process_new_task(message,state)
        print("main message")
        return  # Если пользователь в режиме редактирования, пропускаем обработчик

    message_time = message.date.strftime("%Y-%m-%d %H:%M:%S")  # нужный формат
    promt = f"{message.text}|{message_time}"

    print(f"📩 {promt} ")

    result_trigger = Pauk(message.text)

    if result_trigger is not None:
        result = request_processing(result_trigger,promt,message.from_user.username)
        if isinstance(result, pd.DataFrame):

            for _, row in result.iterrows():

                inline_keyboard = get_inliner(row)
                # Отправляем сообщение с кнопками
                await message.answer(
                    f"📝 {row['task']} ⏰ Время: {row['time']}",
                    reply_markup=inline_keyboard
                )
        else:
            await message.answer(result)

    else:
        print("None")
        gpt = client(get_status_command())
        result = gpt.chat(promt)
        if result == "Нет":
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
