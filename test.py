

def hz():
    promt = f" message.from_user.username | время: message_time | message.text"

    print(promt.split(" | ")[0])

    mass = promt.split(" | ")
    user, date_time, text = mass
    print(mass)
    print(date_time)

from triger import get_lib_trigger as get
def Pauk(text):
    triger_lib = get()
    text  = text.split(" ")
    slovo = text[0]
    for vals in enumerate(triger_lib.values()):
        for val in vals[1]:
            val = val.split(" ")
            if val[0] == slovo:

                return (vals[0],slovo)

    return None


from workDF import work
def chech_time(d_time):
    d_time = "время: 2025-03-15 10:00:00"
    date, time = get_time(d_time)
    df = work()
    status = df.check(date,time)
    return status
def get_time(d_time):
    # d_time = "время: 2025-03-15 10:00:00"
    d_time = d_time.split(" ")
    return (d_time[1],d_time[2])

def add_task(response):
    response = "время: 2025-03-15 10:00:00 | задача: Позвонить маме"

    time, task = response.split(" | ")
    check = chech_time(time)
    if check is None:
        df = work()
        df.add_task(time,task)
        return check
    else:
        pass


# -----------------------------------------------------------------
text = "заssaпиaши на завтра в 10 утра позвонить маме|2025-03-14 17:45:00"
result = Pauk(text)

from GptClient import GPTClient_task as gpt_task
if result is not None:
    df = work()
    index = result[0]
    if index == 0:
        gpt = gpt_task()
        response = gpt.chat(text)
        itog = add_task(response)


else:
    check = add_task(text)
    print(f"data :{check}")

