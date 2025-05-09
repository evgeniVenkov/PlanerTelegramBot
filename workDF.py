import pandas as pd
from pandas import DataFrame


class work():
    def __init__(self):
        self.path_tasks = 'Data_base/tasks.csv'
        self.path_list = 'Data_base/lists.csv'
        self.path_counter = 'Data_base/counter.csv'
        self.path_list_join = 'Data_base/list_join.csv'
        self.path_users = 'Data_base/users.csv'

    def __str__(self):
        return (pd.read_csv(self.path_tasks)).to_string()

    def check(self, data, time):
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

    def add_task(self, response, user_name):
        try:
            # response = "2025-04-07 13:00:00|На концерт"

            print(response)
            time, task = response
            data, time = time.split(" ")

            free = self.check(data, time)
            if free is not None:
                return free
            else:
                df = pd.read_csv(self.path_tasks)

                new_record = {"user": user_name, "date": data, "time": time,
                              "task": task, "join": False, "status": False, "id": self.get_id()}

                df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
                df.to_csv(self.path_tasks, index=False)

                print("Запись добавлена (workDF)")
                return f"Задача: {task} добавлена на {data} {time}"
        except Exception as e:
            print(e)
            return e

    def update_tasks(self, command):
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

    def search_tasks(self, response, user_name):
        # response = '2025-03-21|00:00:00 12:00:00'

        print(response)
        date, t_start, t_end = response

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
            result = df[df["date"] == date]

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
            del (filtered_df['datetime'])
            result = filtered_df

        if result is None:
            result = "Задач в данном диапазоне нет!"
        return result

    def delete_task(self, id):
        id = int(id)
        df = pd.read_csv(self.path_tasks)
        df = df.drop(df[df['id'] == id].index)
        df.to_csv(self.path_tasks, index=False)

    def update_task_id(self, id, new_task):
        id = int(id)
        df = pd.read_csv(self.path_tasks)
        row = df[df['id'] == id]
        row['task'] = new_task
        self.delete_task(id)
        df = pd.read_csv(self.path_tasks)
        df = pd.concat([df, row], ignore_index=True)
        df.to_csv(self.path_tasks, index=False)

    def add_list_item(self, response, user_name):
        # response = ['продукты', 'молоко, яца']

        df = pd.read_csv(self.path_list)
        name_list, values = response
        val = values.split(",")

        # l_join = " ".join(self.get_list_join(user_name, name_list))
        # print(l_join)

        if len(val) > 1:
            mass = []
            for i in val:
                i = i.strip()
                row = {"id": self.get_id(), "user_name": user_name, "list_name": name_list, "record": i, "status": 0,
                       "join": 0}
                mass.append(row)

            new_df = pd.DataFrame(mass)
            df = pd.concat([df, new_df], ignore_index=True)
            result = f"{values}.\nДобавлены в: {name_list}"

        else:
            row = {"id": self.get_id(), "user_name": user_name, "list_name": name_list, "record": values, "status": 0,
                   "join": 0}
            row = pd.DataFrame([row])
            df = pd.concat([df, row], ignore_index=True)
            result = f"{values}.\nДобавлен в: {name_list}"

        df.to_csv(self.path_list, index=False)

        return result

    def search_list(self, list_name: str, user_name: str) -> str | DataFrame:
        # user_name = "Evgen"
        # list_name = "продукты"
        check = self.check_list(user_name, list_name)

        if not isinstance(check, tuple):
            return check

        return self.print_list(check[0])

    def get_list_join(self, user_name: str, name_list: str) -> list[str]:
        df = pd.read_csv(self.path_list_join)
        result = df[(df["user_name"] == user_name) & (df["name_list"] == name_list)]
        if result.empty:
            return f"ошибка в поиске {name_list} {user_name}"
        result = result["list_join"].item()
        split = str(result).split(" ")
        return split

    def check_list(self, user_name: str, list_name: str) -> str | tuple[int, str]:
        df = pd.read_csv(self.path_users)

        if user_name not in df["nik_tg"].values:
            return "Пользователь не найден."

        user_df = df[df["nik_tg"] == user_name]
        str_list = user_df["user_list"].item()
        mass_list = str_list.split(",")

        for val in mass_list:
            index, value = val.split("_")
            if value == list_name:
                return int(index), value

        return f"У вас нет списка {list_name} , добавить?"

    def get_user_lists(self, user_name):
        df = pd.read_csv(self.path_users)
        if user_name not in df["nik_tg"].values:
            print(f"Пользователь: {user_name} не найден.(workDF)")
            return []
        df = df[df["nik_tg"] == user_name]
        str_list = df["user_list"].item()
        mass_list = str_list.split(",")
        mass = []
        for val in mass_list:
            index, value = val.split("_")
            mass.append(value)
        return mass

    def print_list(self, name_list: str,user) -> pd.DataFrame:
        # name_list = ['продукты']
        df = pd.read_csv(self.path_list)
        df = df[df["list_name"] == name_list[0]]
        return df

    def delete_list_item(self, id):
        id = int(id)
        df = pd.read_csv(self.path_list)
        df = df.drop(df[df['id'] == id].index)
        df.to_csv(self.path_list, index=False)


# #
# df = work()
# df.add_task("82","Evgen")
