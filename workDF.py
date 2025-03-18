import pandas as pd

class work():

    def __init__(self):
        self.file_path = 'Data_base/tasks.csv'
    def check(self,data,time):
        df = pd.read_csv(self.file_path)

        # Убеждаемся, что столбцы — это строки без лишних символов
        df["date"] = df["date"].astype(str).str.strip()
        df["time"] = df["time"].astype(str).str.strip()

        data = str(data).strip()  # Приводим входные параметры к строке
        time = str(time).strip()

        exists = ((df["date"] == data) & (df["time"] == time)).any()
        if exists:
            print(f"Запись найдена ✅")
            return df[(df["date"] == data) & (df["time"] == time)]
        else:
            print("Запись отсутствует ❌")
            return None
    def add_task(self,response,user_name):
        try:
            # response = "2025-03-21 18:00:00 | Пойти на выставку"


            time, task = response.split(" | ")
            data, time = time.split(" ")

            free = self.check(data,time)
            if free is not None:
                return free
            else:
                df = pd.read_csv(self.file_path)

                new_record = {"user": user_name, "date":data, "time": time,
                              "task":task[8:],"join":False,"status":False}

                df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
                df.to_csv(self.file_path, index=False)

                print("Запись добавлена (workDF)")
                return "Запись добавлена (workDF)"
        except Exception as e:
            print(e)
            return e


    def update_tasks(self,command):
        """
        Обрабатывает команду от GPT и обновляет таблицу.
        """
        print(f"comand :{command}")

        try:
            df = pd.read_csv(self.file_path)  # Загружаем таблицу

            if command.startswith("cm:"):

                user, comm_type, date, time, task = command[4:].split("|")
                date = date.strip()
                time = time.strip()
                print(f"Comand! \n {date}")

                if comm_type == "add":
                    check = df.check(date, time)
                    if check is None:
                        new_row = pd.DataFrame(
                            {"user": [user], "date": [date], "time": [time], "task": [task], "join": 0, "status": 0})
                        df = pd.concat([df, new_row], ignore_index=True)
                        message = f"Добавлена новая задача: {date} {time} - {task}"
                    else:
                        message = f"Данное время и дата заняты, перезаписать?"

                elif comm_type == "Update":

                    message = f"♻️ Задача будет обновлена: {task} {time} -"

            else:
                return "Ошибка: неизвестная команда."

            df.to_csv(self.file_path, index=False)  # Сохраняем изменения
            return message

        except Exception as e:
            return f"Ошибка при обновлении задач: {e}"

#
#
# work = work()
# work.add_task("dada","adsdsad")