import pandas as pd
import os
import workDF
from GptClient import GPTClient
from promt import get_task_promt as GP

df = workDF.work()
FILE_PATH = "Data_base/tasks.csv"
# Создаём таблицу, если её нет
if not os.path.exists(FILE_PATH):
    df = pd.DataFrame(columns=["user", "date", "time", "task", "join","status"])
    df.to_csv(FILE_PATH, index=False)

def command(index,mess_text):
    # mess_text = "запиши завтра в 7 к стоматологу|2025-02-27 07:45:24"
    if index == 0:
        gpt = GPTClient(GP())
        response = gpt.chat(mess_text)
        itog = df.add_task(response)

    else:
        itog = "индекса нет"
        print(f"{itog}")

    return itog



command(0,"dad")
# print(update_tasks("cm: Microboss|add| 2025-03-20 | 15:01 | пойти на выставку"))