import pandas as pd
import os

FILE_PATH = "tasks.csv"

# Создаём таблицу, если её нет
if not os.path.exists(FILE_PATH):
    df = pd.DataFrame(columns=["Дата", "Время", "Задача"])
    df.to_csv(FILE_PATH, index=False)

def update_tasks(command):
    """
    Обрабатывает команду от GPT и обновляет таблицу.
    Поддерживаемые команды:
    - ad: ДАТА | ВРЕМЯ | ЗАДАЧА  (добавить)
    - cr: ДАТА | ВРЕМЯ | НОВАЯ ЗАДАЧА  (изменить)
    """
    print(command)
    try:
        df = pd.read_csv(FILE_PATH)  # Загружаем таблицу

        # Определяем тип команды (ad - добавить, cr - изменить)
        if command[3:0].startswith("ad: "):
            date, time, task = command[4:].split("|")
            new_row = pd.DataFrame({"Дата": [date], "Время": [time], "Задача": [task]})
            df = pd.concat([df, new_row], ignore_index=True)
            message = f"✅ Добавлена новая задача: {date} {time} - {task}"

        elif command.startswith("cr: "):
            date, time, new_task = command[4:].split("|")
            df.loc[(df["Дата"] == date) & (df["Время"] == time), "Задача"] = new_task
            message = f"♻️ Задача обновлена: {date} {time} - {new_task}"

        else:
            return "❌ Ошибка: неизвестная команда."

        df.to_csv(FILE_PATH, index=False)  # Сохраняем изменения
        return message

    except Exception as e:
        return f"❌ Ошибка при обновлении задач: {e}"
