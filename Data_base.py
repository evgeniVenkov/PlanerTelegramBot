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
    mess_text = "добавь купить хлеб|2025-02-27 07:45:24"

    gpt_add = client(get_task(user_name), model="gpt-4-turbo")
    response = gpt_add.chat(mess_text)
    mess_split = response.split("|")

    if mess_split[0] == "task":
        print(response[5:])
        itog = df.add_task(response[5:],user_name)

    else:
        print(mess_split[0])
        itog = df.add_list_item(response,user_name)
    return itog

def command_search(mess_text, user_name):
    # mess_text = "что нужно купить в аптеке|2025-03-20 07:45:24"
    # user_name = "Evgen"

    gpt_search = client(get_search(user_name), model="gpt-4-turbo")
    response = gpt_search.chat(mess_text)
    split = response.split("|")
    if split[0] == "list":
        itog = df.search_list(user_name, split[1])
        tip = "list"
    else:
        itog = df.search_tasks(response, user_name)
        tip = "task"
    return itog, tip

def command_delete(id):
    df.delete_task(id)
def command_update_id(id, new_task):
    df.update_task_id(id,new_task)


# print(command_add(0,"Microgboss"))
