import pandas as pd
import os
import workDF

wdf = workDF.work()

FILE_PATH = "tasks.csv"

# Создаём таблицу, если её нет
if not os.path.exists(FILE_PATH):
    df = pd.DataFrame(columns=["user", "date", "time", "task", "join","status"])
    df.to_csv(FILE_PATH, index=False)

def update_tasks(command):
    """
    Обрабатывает команду от GPT и обновляет таблицу.
    """
    print(f"comand :{command}")

    try:
        df = pd.read_csv(FILE_PATH)  # Загружаем таблицу


        if command.startswith("cm:"):
            print(True)
            user,comm_type,date,time,task = command[4:].split("|")
            print(date)


            if comm_type == "add":
                check = wdf.check(date,time)
                if check is None:
                    new_row = pd.DataFrame({"user": [user], "date": [date], "time": [time], "task": [task], "join": 0, "status": 0})
                    df = pd.concat([df, new_row], ignore_index=True)
                    message = f"Добавлена новая задача: {date} {time} - {task}"
                else:
                    message = f"Данное время и дата заняты, перезаписать?"

            elif comm_type == "Update":

                message = f"♻️ Задача будет обновлена: {task} {time} -"

        else:
            return "Ошибка: неизвестная команда."

        df.to_csv(FILE_PATH, index=False)  # Сохраняем изменения
        return message

    except Exception as e:
        return f"Ошибка при обновлении задач: {e}"




# print(update_tasks("cm: Microboss|add| 2025-03-20 | 15:01 | пойти на выставку"))