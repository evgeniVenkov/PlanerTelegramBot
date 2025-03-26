from unittest import result

import pandas as pd

def result_df(result):
    df = pd.read_csv("Data_base/tasks.csv")
    df  = df.iloc[0]

    if isinstance(df,pd.Series):
        mass =df["date"],df["time"],df["task"]
        return mass


text = "Существует много способов заработать деньги, включая работу, бизнес, инвестиции и т.д. Важно выбрать подходящий способ и быть готовым к усердной работе и умелому управлению финансами."
split = text.split(" ")
coun_slov = 10
if len(split) // coun_slov >= 1:
    for index, val in enumerate(split):
        if index % coun_slov == 0:
            split[index] = f"{val} \n"
split = " ".join(split)

print(split)


