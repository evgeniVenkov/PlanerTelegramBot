import pandas as pd

class work():

    def __init__(self):
        self.df = pd.read_csv("tasks.csv")

    def check(self,data,time):
        df = self.df

        exists = ((df["date"] == data) & (df["time"] == time)).any()
        if exists:
            print(f"Запись найдена ✅")
            return df[(df["date"] == data) & (df["time"] == data)]
        else:
            print("Запись отсутствует ❌")
            return None

#
# wdf = work()
#
# date_to_check = "2025-03-20"
# time_to_check = "15:00"
#
#
# # Убедимся, что столбцы хранятся как строки (на всякий случай)
#
#
#
# print(type(wdf.check(date_to_check,time_to_check)))