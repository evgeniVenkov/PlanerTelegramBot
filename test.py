import pandas as pd


def check_list(user_name: str, list_name: str) -> str | tuple[int, str]:
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


def print_list(list_id: int) -> pd.DataFrame:
    df = pd.read_csv("./Data_base/lists.csv")
    df = df[df["list_id"] == list_id]
    return df


# Пример использования
user_name = "Evgen"
list_name = "электроника"

print(id)
