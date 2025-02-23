import os
from dotenv import load_dotenv
import openai
from dotenv import load_dotenv
import Data_base
import promt
load_dotenv()
api_key = os.getenv("KEY") # Берём ключ через функцию




class GPTClient:
    def __init__(self):
        """Инициализация API клиента и загрузка ключа"""
        load_dotenv()
        self.client = openai.OpenAI(api_key=api_key)  # Новый клиент
        self.history = []  # История диалога
        self.system_prompt = (promt.get())
        self.first_request = True  # Флаг первого запроса

    def chat(self, user_message):
        """Отправляет запрос в GPT и получает ответ"""
        if not api_key:
            return " Ошибка: API-ключ OpenAI не найден."

        # Добавляем системное сообщение при первом запросе
        if self.first_request:
            self.history.append({"role": "system", "content": self.system_prompt})
            self.first_request = False

        # Добавляем сообщение пользователя
        self.history.append({"role": "user", "content": user_message})

        try:
            response = self.client.chat.completions.create(  # Новый синтаксис
                model="gpt-3.5-turbo",
                messages=self.history,
                temperature=0.7
            )

            bot_reply = response.choices[0].message.content
            self.history.append({"role": "assistant", "content": bot_reply})

            if bot_reply.startswith("ad:") or bot_reply.startswith("cr:"):
                bot_reply = Data_base.update_tasks(bot_reply)

            return bot_reply
        except Exception as e:
            return f" Ошибка при обращении к GPT: {e}"


client = GPTClient()

prom = "что ты умеешь?"
response = client.chat(prom)
print(response)