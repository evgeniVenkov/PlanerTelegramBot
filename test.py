import pandas as pd





new_record = {"user": "user_name", "date": "data", "time": "time",
                              "task": "task", "join": False, "status": False, "id": 0}

df = pd.DataFrame([new_record])
df.to_csv('Data_base/tasks.csv', index=False)