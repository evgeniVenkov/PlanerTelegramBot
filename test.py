from typing import Tuple, Any

import pandas as pd

df = pd.read_csv("./Data_base/lists.csv")


def chek_list():
    pass


# Метод для проверки доступа
def check_access(user_name: str, list_name: str) -> str | tuple[int, str]:
    df = pd.read_csv("./Data_base/users.csv")

    if user_name not in df["nik_tg"].values:
        return "Пользователь не найден."

    user_df = df[df["nik_tg"] == user_name]
    str_list = user_df["user_list"].item()
    mass_list = str_list.split(",")

    for val in mass_list:
        index, value = val.split("_")
        if value == list_name:
            return int(index), value

    return "У вас нет данного списка, добавить?"


# Пример использования
user_name = "Evgen"
list_name = "электроника"

result = check_access(user_name, list_name)
print(result)
