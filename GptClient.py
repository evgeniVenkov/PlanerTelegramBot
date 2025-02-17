import os
import openai
from dotenv import load_dotenv
from key import get_key  # Загружаем API-ключ

api_key = get_key()  # Берём ключ через функцию

class GPTClient:
    def __init__(self):
        """Инициализация API клиента и загрузка ключа"""
        load_dotenv()
        self.client = openai.OpenAI(api_key=api_key)  # Новый клиент
        self.history = []  # История диалога
        self.system_prompt = (
            "Ты бот-планировщик. Твои задачи:\n"
            "1. Добавлять задачи пользователей.\n"
            "2. Редактировать и удалять задачи.\n"
            "3. Отвечать вежливо и кратко.\n"
            "Формат команд:\n"
            "Для записи новой задачи\n "
            "- ad: дата| задача.\n"
            "пример: ad: 19.02.2025| поход к врачу\n "
            "Для перезаписи задачи\n"
            "- cr: дата| задача.\n"
            "пример: cr: 19.02.2025| поход в музей\n"

        )
        self.first_request = True  # Флаг первого запроса

    def chat(self, user_message):
        """Отправляет запрос в GPT и получает ответ"""
        if not api_key:
            return "❌ Ошибка: API-ключ OpenAI не найден."

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

            return bot_reply
        except Exception as e:
            return f"❌ Ошибка при обращении к GPT: {e}"


# client = GPTClient()
#
# prom = "в среду в 9 утра к врачу?"
# response = client.chat(prom)
# print(response)