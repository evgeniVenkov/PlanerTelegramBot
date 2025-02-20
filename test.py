
command = "ad: ДАТА | ВРЕМЯ | ЗАДАЧА"

if command.startswith("ad:"):

    date, time, task = command[4:].split(" | ")
    print(date, time, task)