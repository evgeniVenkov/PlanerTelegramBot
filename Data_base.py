import pandas as pd
import os
import workDF
from client import client
from promt import get_task, get_search

df = workDF.work()
FILE_PATH = "Data_base/tasks.csv"
# Создаём таблицу, если её нет
if not os.path.exists(FILE_PATH):
    df = pd.DataFrame(columns=["user", "date", "time", "task", "join","status"])
    df.to_csv(FILE_PATH, index=False)

def command_add(mess_text,user_name):
    # mess_text = "запиши завтра в 7 к стоматологу|2025-02-27 07:45:24"

    gpt_add = client(get_task())
    response = gpt_add.chat(mess_text)
    itog = df.add_task(response,user_name)

    return itog

def command_search(mess_text, username):
    # mess_text = "покажи задачи на завтра|2025-03-20 07:45:24"

    gpt_search = client(get_search())
    response = gpt_search.chat(mess_text)
    itog = df.search_tasks(response, username)
    return itog

# print(command_search(0,"Microgboss"))
