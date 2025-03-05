import os
from flask import Flask, request
import requests

app = Flask(__name__)

# Получаем токен из переменных окружения
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise Exception("TELEGRAM_BOT_TOKEN не установлен в переменных окружения")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        # Пример обработки команды: эхо-ответ
        reply = f"Ты сказал: {text}"
        send_message(chat_id, reply)
    return {"ok": True}

if __name__ == "__main__":
    app.run()
