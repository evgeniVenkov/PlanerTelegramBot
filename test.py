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
    count = 0
    for vals in enumerate(triger_lib.values()):
        for val in vals[1]:
            val = val.split(" ")
            if val[0] == slovo:
                print("Yes!")
                print(

        print(vals[1])
        count +=1
        if count >= 3:
            break



text = "запиши на завтра в 10 утра позвонить маме"

Pauk(text)
