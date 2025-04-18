import pandas as pd
from pytz import timezone

moscow_tz = timezone("Europe/Moscow")
message_time = message.date.astimezone(moscow_tz).strftime("%Y-%m-%d %H:%M:%S")
