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
from Data_base import command_add,command_search,command_delete,command_update_id
from client import client
from promt import get_сhat,get_status_command,get
from aiogram.fsm.storage.memory import MemoryStorage
from workDF import work
from pytz import timezone



# Загружаем токен из .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

df = work()

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

@router.message(EditTaskState.waiting_for_new_task)
async def process_new_task(message: Message, state: FSMContext):
    new_task = message.text.strip()  # Убираем лишние пробелы
    data = await state.get_data()

    task_id = data.get("task_id")  # Получаем ID задачи из состояния

    if not task_id:
        await message.answer("Ошибка: не удалось получить ID задачи.")
        await state.clear()
        return

    command_update_id(task_id, new_task)  # Обновляем задачу в БД или другом хранилище

    await message.answer(f"✅ Задача обновлена: {new_task}")
    await state.clear()  # Сбрасываем состояние
# ---------------------------------------------------------------------
@router.callback_query(F.data.startswith("EditTask_"))
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
@router.callback_query(F.data.startswith("DeleteTask_"))
async def delete_task(callback: CallbackQuery):
    task_name = callback.data.split("_" )[2]
    id = callback.data.split("_")[1]
    command_delete(id)

    await callback.message.delete()  # Удаляем сообщение с задачей
    await callback.message.answer(f"🗑 Задача {task_name}")
    await callback.answer()  # Подтверждаем, что запрос был обработан
@router.callback_query(F.data.startswith("CompliteTask_"))
async def complite_task(callback: CallbackQuery):
    task_name = callback.data.split("_")[2]  # Получаем название задачи
    await callback.message.delete()  # Удаляем сообщение с задачей
    await callback.message.answer(f"👍Задача '{task_name}' Выполнена!=!")
    await callback.answer()  # Подтверждаем, что запрос был обработан
@router.callback_query(F.data.startswith("DeleteList_"))
async def delete_list(callback: CallbackQuery):
    item_name = callback.data.split("_" )[2]
    id = callback.data.split("_")[1]
    df.delete_list_item(id)
    print(f"tyt(main 102) id{id}")
    await callback.message.delete()  # Удаляем сообщение с задачей
    await callback.message.answer(f"🗑 {item_name}")
    await callback.answer()  # Подтверждаем, что запрос был обработан
@router.callback_query(F.data.startswith("CompliteList_"))
async def complite_list(callback: CallbackQuery):
    task_name = callback.data.split("_")[2]  # Получаем название задачи
    await callback.message.delete()  # Удаляем сообщение с задачей
    await callback.message.answer(f"{task_name} куплено👍")
    await callback.answer()  # Подтверждаем, что запрос был обработан
#----------------------------------------------------------------------
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
# ----------------------------------------------------------------
def request_processing(result_trigger, promt, username):

    if result_trigger == "add":
        result = command_add(promt, username)
        tip = "add"
    elif result_trigger == "search":
        print(f"tip: search")
        result, tip = command_search(promt, username)
    else:
        tip = "error"
        result =f"(main)\n{result_trigger}"
        print(result)

    return result,tip
def get_inliner_task(row):
    # Создаём билдера для клавиатуры
    builder = InlineKeyboardBuilder()

    # Добавляем кнопки
    builder.button(
        text="✏️ Редактировать",
        callback_data=f"EditTask_{row['id']}_{row['task']}"
    )
    builder.button(
        text="🗑 Удалить",
        callback_data=f"DeleteTask_{row['id']}_{row['task']}"
    )
    builder.button(
        text="👍 выполнена!",
        callback_data=f"CompliteTask_{row['id']}_{row['task']}"
    )

    # Создаём InlineKeyboardMarkup из билдера
    return builder.as_markup()
def get_inliner_list(row):
    # Создаём билдера для клавиатуры
    builder = InlineKeyboardBuilder()

    # Добавляем кнопки
    builder.button(
        text="🗑",
        callback_data=f"DeleteList_{row['id']}_{row['record']}"
    )
    builder.button(
        text="👍",
        callback_data=f"CompliteList_{row['id']}_{row['record']}"
    )

    # Создаём InlineKeyboardMarkup из билдера
    return builder.as_markup()
# ---------------------------------------------------------------------
@dp.message()
async def echo_message(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == EditTaskState.waiting_for_new_task.state:
        await process_new_task(message,state)
        print("main message")
        return  # Если пользователь в режиме редактирования, пропускаем обработчик

    user = message.from_user.username

    moscow_tz = timezone("Europe/Moscow")
    message_time = message.date.astimezone(moscow_tz).strftime("%Y-%m-%d %H:%M:%S") # нужный формат

    promt = f"{user}|{message_time}|{message.text}"

    print(f"📩 {promt} ")

    sys_prom = get()
    gpt = client(sys_prom,model="gpt-4o")
    response = gpt.chat(promt)

    tip = None
    result = None


    if response[:3] == "cm:":
        mass = response[3:].split('|')
        tip = mass[1]

        if tip == "p_task":
            result = df.search_tasks(mass[2:], user)
        elif tip == "add_task":
            result = df.add_task(mass[2:4], user)
        elif tip == "add_item":
            result = df.add_list_item(mass[2:], user)
        elif tip == "del_item":
            pass
        elif tip == "p_list":
            result = df.print_list(mass[2])
    else:
        result = response
    if tip == "p_list":
        if isinstance(result, pd.DataFrame):
            for _, row in result.iterrows():
                inline_keyboard = get_inliner_list(row)
                await message.answer(
                    f"📝 {row['record']}",
                    reply_markup=inline_keyboard
                )
            if result.empty:
                await message.answer("Список пуст")
    elif tip == "p_task":
        if isinstance(result, pd.DataFrame):

            for _, row in result.iterrows():
                inline_keyboard = get_inliner_task(row)
                # Отправляем сообщение с кнопками
                await message.answer(
                    f"📝 {row['task']} ⏰ Время: {row['time']}",
                    reply_markup=inline_keyboard
                )
        if result.empty:
            await message.answer("нет задач!")
    else:
        await message.answer(result)
async def main():
    print("✅ Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



