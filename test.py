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
def search_list(user_name: str, list_name: str):
    df = pd.read_csv(self.path_list)
    df = df[df["name_list"]==list_name]
    df = df[(df['user_name']==user_name) | (df['join']==user_name)]


mass = list_join("Evgen","электроника")
print(" ".join(mass))