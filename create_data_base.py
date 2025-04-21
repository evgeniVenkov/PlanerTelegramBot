import pandas as pd

row = {"count_id":60}

df = pd.DataFrame([row])
df.to_csv("Data_base/counter.csv")