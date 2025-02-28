promt = f" message.from_user.username | время: message_time | message.text"

print(promt.split(" | ")[0])

mass = promt.split(" | ")
user, date_time, text = mass
print(mass)
print(date_time)