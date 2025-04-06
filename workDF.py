import pandas as pd


class work():
    def __init__(self):
        self.path_tasks = 'Data_base/tasks.csv'
        self.path_list = 'Data_base/lists.csv'
        self.path_counter = 'Data_base/counter.csv'
    def __str__(self):
        return (pd.read_csv(self.path_tasks)).to_string()


    def check(self,data,time):
        df = pd.read_csv(self.path_tasks)

        df["date"] = df["date"].astype(str).str.strip()
        df["time"] = df["time"].astype(str).str.strip()

        data = str(data).strip()
        time = str(time).strip()

        exists = ((df["date"] == data) & (df["time"] == time)).any()
        if exists:
            print(f"Запись найдена ✅")
            return df[(df["date"] == data) & (df["time"] == time)]
        else:
            print("Запись отсутствует ❌")
            return None
    def get_id(self):
        df = pd.read_csv(self.path_counter)

        last_row = df.iloc[-1]
        count = int(last_row["count_id"]) + 1
        last_row["count_id"] = count

        df = pd.concat([df, pd.DataFrame([last_row])], ignore_index=True)
        df.to_csv(self.path_counter, index=False)

        return count
    def add_task(self,response,user_name):
        try:
            # response = "2025-03-21 18:00:00 | Пойти на выставку"

            time, task = response.split(" | ")
            data, time = time.split(" ")

            free = self.check(data,time)
            if free is not None:
                return free
            else:
                df = pd.read_csv(self.path_tasks)

                new_record = {"user": user_name, "date":data, "time": time,
                              "task":task,"join":False,"status":False, "id":self.get_id()}

                df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
                df.to_csv(self.path_tasks, index=False)

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
            df = pd.read_csv(self.path_tasks)  # Загружаем таблицу

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

            df.to_csv(self.path_tasks, index=False)  # Сохраняем изменения
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

        df = pd.read_csv(self.path_tasks)
        df = df[df["user"] == user_name]

        df["date"] = pd.to_datetime(df["date"]).dt.date
        df["time"] = pd.to_datetime(df["time"], format="%H:%M:%S").dt.time

        if t_start == day_time and t_end == day_time:
            print("day")
            result =  df[df["date"] == date]

        elif t_start == t_end:
            print("hour")
            task = df[(df['date'] == date) & (df['time'] == t_start)]
            result = task if not task.empty else None

        else:
            df['datetime'] = df.apply(lambda row: pd.Timestamp.combine(row['date'], row['time']), axis=1)

            filtered_df = df[
                (df['datetime'].dt.date == date) &
                (df['datetime'].dt.time >= t_start) &
                (df['datetime'].dt.time <= t_end)
                ]
            del(filtered_df['datetime'])
            result = filtered_df


        if result.empty:
            result = "Задач в данном диапазоне нет!"
        return result
    def delete_task(self,id):
        id = int(id)
        df = pd.read_csv(self.path_tasks)
        df = df.drop(df[df['id'] == id].index)
        df.to_csv(self.path_tasks, index=False)
    def update_task_id(self,id,new_task):
        id = int(id)
        df = pd.read_csv(self.path_tasks)
        row = df[df['id']==id]
        row['task'] = new_task
        self.delete_task(id)
        df = pd.read_csv(self.path_tasks)
        df = pd.concat([df, row], ignore_index=True)
        df.to_csv(self.path_tasks, index=False)
    def add_list_item(self,response,user_name):
        df = pd.read_csv(self.path_list)
        # response ="продуктовый магазин|Картошка, марковка"

        name_list, values = response.split("|")
        val = values.split(",")
        if len(val) > 1:
            mass = []
            for i in val:
                i = i.strip()
                row = {"user_name": user_name, "name_list": name_list, "record": i, "status": 0, "join": 0}
                mass.append(row)

            new_df = pd.DataFrame(mass)
            df = pd.concat([df, new_df], ignore_index=True)


        else:
            row = {"user_name": user_name, "name_list": name_list, "record": val[0].strip(), "status": 0, "join": 0}
            row = pd.DataFrame([row])
            df = pd.concat([df, row], ignore_index=True)

        df.to_csv(self.path_list, index=False)

        return f"{values}.\nДобавлены в: {name_list}"

    def search_list(self,user_name, list_name):
        # user_name = "Evgen"
        # list_name = "продуктовый магазин"

        df = pd.read_csv(self.path_list)
        df = df[df["name_list"]==list_name]
        df = df[(df['user_name']==user_name) | (df['join']==user_name)]
        return df


#
#
# df = work()
# print(df.search_list("ads", "Evgen"))