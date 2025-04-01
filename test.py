from unittest import result

import pandas as pd

def result_df(result):
    df = pd.read_csv("Data_base/tasks.csv")
    df  = df.iloc[0]

    if isinstance(df,pd.Series):
        mass =df["date"],df["time"],df["task"]
        return mass

def hz():
    text = "Существует много способов заработать деньги, включая работу, бизнес, инвестиции и т.д. Важно выбрать подходящий способ и быть готовым к усердной работе и умелому управлению финансами."
    split = text.split(" ")
    coun_slov = 10
    if len(split) // coun_slov >= 1:
        for index, val in enumerate(split):
            if index % coun_slov == 0:
                split[index] = f"{val} \n"
    split = " ".join(split)

    print(split)

df = pd.read_csv("Data_base/counter.csv")

last_row = df.iloc[-1]  # Последняя строка
count = int(last_row["count_id"]) + 1  # Новый count_id

# Создаём новую строку, копируя значения из предыдущей, но увеличивая count_id
new_row = last_row.copy()
new_row["count_id"] = count

# Добавляем новую строку в DataFrame
df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

df.to_csv("Data_base/counter.csv", index=False)
