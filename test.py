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

text = "запиши на завтра в 10 утра позвонить маме|2025-03-14 17:45:00"

result = Pauk(text)
from GptClient import GPTClient_task as gpt_task

if result is not None:
    index = result[0]
    if index == 0:
        gpt = gpt_task()
        response = gpt.chat(text)
        print(response)

else:
    print("NONE")
