import pandas as pd

class work():

    def __init__(self):
        self.df = pd.read_csv("tasks.csv")

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
#
#
# wdf = work()
#
# date_to_check = "2025-03-07"
# time_to_check = "18:30"
#
#
# print(type(wdf.check(date_to_check,time_to_check)))