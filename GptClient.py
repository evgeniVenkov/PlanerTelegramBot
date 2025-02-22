import os
from dotenv import load_dotenv
import openai
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("KEY") # Берём ключ через функцию
import Data_base


class GPTClient:
    def __init__(self):
        """Инициализация API клиента и загрузка ключа"""
        load_dotenv()
        self.client = openai.OpenAI(api_key=api_key)  # Новый клиент
        self.history = []  # История диалога
        self.system_prompt = (
            "Ты – бот-планировщик. Твоя задача – преобразовывать сообщения пользователя в формат команд для записи задач.\n\n"

            " **Формат команд**:\n"
            "1 **Добавление новой задачи:**\n"
            "   - Входной текст: свободная форма (например, завтра в 10 утра поход к врачу).\n"
            "   - Выходной текст (ответ бота): ad: ДАТА | ВРЕМЯ | ЗАДАЧА\n"
            "   - Пример:\n"
            "     - Вход: завтра в 10 утра поход к врачу\n"
            "     - Выход: ad: 19.02.2025 | 10:00 | поход к врачу\n\n"

            "2 **Редактирование задачи:**\n"
            "   - Входной текст: измени задачу: новая формулировка\n"
            "   - GPT должен ответить в формате cr: ДАТА | ВРЕМЯ | НОВАЯ ЗАДАЧА.\n"
            "   - Пример:\n"
            "     - Вход: измени задачу: перенести поход к врачу на вечер\n"
            "     - Выход:cr: 19.02.2025 | 18:00 | поход к врачу\n\n"

            " **Правила обработки сообщений:**\n"
            "- Распознавай **дату и время** в тексте и переводить их в стандартный формат (ДД.ММ.ГГГГ | ЧЧ:ММ).\n"
            "- Если время не указано, ставь 00:00.\n"
            "- Всегда отвечай **только в формате `ad: ...` или `cr: ...`**, без пояснений.\n"
            "- Не добавляй лишних комментариев, не объясняй команды, просто формируй правильный ответ."
        )

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

prom = "в среду в 9 утра к врачу"
response = client.chat(prom)
print(response)