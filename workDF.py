import pandas as pd

class work():

    def __init__(self):
        self.file_path = 'tasks.csv'
        try:
            self.df = pd.read_csv(self.file_path)
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=["ID", "Name", "Age"])

    def check(self,data,time):
        df = self.df.copy()  # Создаём копию на всякий случай

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

    def add_task(self,data,task):
        try:

            data, time = self.get_time(data)
            print(data)

            new_record = {"user": None, "date":data, "time": time,
                          "task":task[8:],"join":False,"status":False}
            df = pd.concat([self.df, pd.DataFrame([new_record])], ignore_index=True)
            df.to_csv(self.file_path, index=False)

            print("Запись добавлена (workDF)")
        except Exception as e:
            print(e)

    def get_time(self,d_time):
        # d_time = "время: 2025-03-15 10:00:00"
        d_time = d_time.split(" ")
        return (d_time[1], d_time[2])
    def print_df(self):
        self.df.head()
# wdf = work()
#
# date_to_check = "2025-03-07"
# time_to_check = "18:30"
#
#
# print(type(wdf.check(date_to_check,time_to_check)))