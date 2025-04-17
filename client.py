import os
import openai
from dotenv import load_dotenv
from promt import get
from workDF import work

load_dotenv()
api_key = os.getenv("KEY")


class client:
    def __init__(self,promt,count_history = 3, model = "gpt-3.5-turbo"):
        """Инициализация API клиента и загрузка ключа"""
        self.client = openai.OpenAI(api_key=api_key)  # Новый клиент
        self.history = []  # История диалога
        self.system_prompt = promt
        self.first_request = True  # Флаг первого запроса
        self.count_history = count_history
        self.model = model
    def chat(self, user_message):
        # #хз зачем потом придумаю :)
        # mass = user_message.split(" | ")
        # user, date_time, text = mass


        """Отправляет запрос в GPT и получает ответ"""
        if not api_key:
            return " Ошибка: API-ключ OpenAI не найден."
        if len(self.history) >= self.count_history:
            self.history = []
            self.first_request = False


        if self.first_request:
            self.history.append({"role": "system", "content": self.system_prompt})
            self.first_request = False


        self.history.append({"role": "user", "content": user_message})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                temperature=0.7
            )

            bot_reply = response.choices[0].message.content
            self.history.append({"role": "assistant", "content": bot_reply})

            print(f"Ответ гпт:(ckient) {bot_reply}")

            # if bot_reply.startswith("cm:"):
            #     bot_reply = Data_base.update_tasks(bot_reply)

            return bot_reply
        except Exception as e:
            return f" Ошибка при обращении к GPT: {e}"

sys_prom = get()
client = client(sys_prom, model="gpt-4-turbo")
prom = "Evgen|2025-04-13 18:25:03|завтра отвезти тещу к врачу"
response = client.chat(prom)

df = work()

if response[:3] == "cm:":
    mass = response[3:].split('|')
    user = mass[0]

    tip = mass[1]
    if tip == "p_task":
        result = df.search_tasks(mass[2:],user)
    elif tip == "add_task":
        result = df.add_task(mass[2:4],user)
    elif tip == "add_item":
        pass
    elif tip == "del_item":
        pass
    elif tip == "p_list":
        pass
