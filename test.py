from unittest import result

import pandas as pd

def result_df(result):
    df = pd.read_csv("Data_base/tasks.csv")
    df  = df.iloc[0]

    if isinstance(df,pd.Series):
        mass =df["date"],df["time"],df["task"]
        return mass





res = result_df(1)

print(res)