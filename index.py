import os
import random
import requests
from flask import Flask, request

app = Flask(__name__)

# Получаем токен из переменных окружения
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise Exception("TELEGRAM_BOT_TOKEN не установлен в переменных окружения")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# Список подарков (можно расширять)
GIFTS = [
    "🌟 Поздравляю! Ты получил звезду!",
    "🎁 Вот твой подарок!",
    "💎 Ты выиграл бриллиант!",
    "🍀 Лаки-чарм для удачи!",
    "🎉 От души – наслаждайся подарком!"
]

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")
        
        if text.startswith("/start"):
            welcome = ("Привет!\n"
                       "Отправь команду /gift, чтобы получить случайный подарок!")
            send_message(chat_id, welcome)
        elif text.startswith("/gift"):
            gift = random.choice(GIFTS)
            send_message(chat_id, gift)
        else:
            send_message(chat_id, "Неизвестная команда. Попробуй /start или /gift.")
    return {"ok": True}

if __name__ == "__main__":
    app.run()
