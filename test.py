import pandas as pd

def create_df():
    new = [
        {"user_name": "Evgen", "name_list": "продуктовый магазин", "list_join": "Dasha"},
        {"user_name": "Evgen", "name_list": "магазин электроники", "list_join": "Max, Ivan"},
        {"user_name": "Evgen", "name_list": "аптека", "list_join": "Olga"},
        {"user_name": "Evgen", "name_list": "пекарня", "list_join": "Vera, Sasha, Oleg"},
        {"user_name": "Evgen", "name_list": "супермаркет", "list_join": "Artem"}
    ]

    df = pd.DataFrame(new)

    df.to_csv("Data_base/list_join.csv")
    #
# print(df)

def list_join(user_name: str, name_list:str) -> list[str]:

    df = pd.read_csv("Data_base/list_join.csv")
    result = df[(df["user_name"] == user_name) & (df["name_list"] == name_list)]
    if result.empty:
        return f"ошибка в поиске {name_list} {user_name}"
    result = result["list_join"].item()
    split = str(result).split(" ")
    return split



mass = list_join("Evgen","электроника")
print(" ".join(mass))