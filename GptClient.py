import os
import openai
from dotenv import load_dotenv
from key import get_key as GK
class GPTClient:
    def __init__(self):
        """Инициализация API клиента и загрузка ключа"""
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.history = []  # История диалога
        self.system_prompt = (
            "Ты бот-планировщик. Твои задачи:\n"
            "1. Добавлять задачи пользователей.\n"
            "2. Редактировать и удалять задачи.\n"
            "3. Отвечать вежливо и кратко.\n"
            "Формат команд:\n"
            "- 'ad: купить молоко'.\n"
            "- 'cr: купить хлеб вместо молока'."
        )
        self.first_request = True  # Флаг первого запроса

    def chat(self, user_message):
        """Обрабатывает запрос пользователя и отправляет его в GPT"""
        if not self.api_key:
            return "❌ Ошибка: API-ключ OpenAI не найден."

        # Добавляем системный промпт только при первом запросе
        if self.first_request:
            self.history.append({"role": "system", "content": self.system_prompt})
            self.first_request = False

        # Добавляем сообщение пользователя
        self.history.append({"role": "user", "content": user_message})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Можно заменить на другую модель
                messages=self.history,
                temperature=0.7
            )

            bot_reply = response["choices"][0]["message"]["content"]
            self.history.append({"role": "assistant", "content": bot_reply})

            return bot_reply
        except Exception as e:
            return f"❌ Ошибка при обращении к GPT: {e}"

