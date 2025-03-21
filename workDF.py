import pandas as pd





class work():

    def __init__(self):
        self.file_path = 'Data_base/tasks.csv'
    def __str__(self):
        return (pd.read_csv(self.file_path)).to_string()


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
    def get_id(self):
        df = pd.read_csv(self.file_path)
        last_row = df.iloc[-1]
        return int(last_row["id"]) + 1
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
                              "task":task,"join":False,"status":False, "id":self.get_id()}

                df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
                df.to_csv(self.file_path, index=False)

                print("Запись добавлена (workDF)")
                return f"Задача: {task} добавлена на {data} {time}"
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
    def search_tasks(self,response,user_name):
        # response = '2025-03-21 | 13:00:00 13:00:00'

        date, time = response.split(" | ")
        t_start, t_end = time.split(" ")

        day_time = "00:00:00"
        day_time = pd.to_datetime(day_time, format="%H:%M:%S").time()

        date = pd.to_datetime(date).date()
        t_start = pd.to_datetime(t_start, format="%H:%M:%S").time()
        t_end = pd.to_datetime(t_end, format="%H:%M:%S").time()

        df = pd.read_csv(self.file_path)
        df = df[df["user"] == user_name]

        df["date"] = pd.to_datetime(df["date"]).dt.date
        df["time"] = pd.to_datetime(df["time"], format="%H:%M:%S").dt.time

        if t_start == day_time and t_end == day_time:
            print("day")
            return df[df["date"] == date]

        elif t_start == t_end:
            print("hour")
            task = df[(df['date'] == date) & (df['time'] == t_start)]
            return task if not task.empty else None

        else:
            df['datetime'] = df.apply(lambda row: pd.Timestamp.combine(row['date'], row['time']), axis=1)

            filtered_df = df[
                (df['datetime'].dt.date == date) &
                (df['datetime'].dt.time >= t_start) &
                (df['datetime'].dt.time <= t_end)
                ]
            del(filtered_df['datetime'])
            return filtered_df
    def delete_task(self,id):
        df = pd.read_csv(self.file_path)
        df = df.drop(df[df['id'] == id].index)
        df.to_csv(self.file_path, index=False)
#

df = work()
print(df)
df.delete_task(4)