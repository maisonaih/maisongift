import os
import random
import requests
from flask import Flask, request
from database import get_user, update_user_stars, create_user
from helpers import get_random_prize

app = Flask(__name__)

# Получаем токен бота из переменной окружения
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise Exception("TELEGRAM_BOT_TOKEN не установлен")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# Обработчик отправки сообщений через Telegram API
def send_message(chat_id, text, keyboard=None):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if keyboard:
        payload["reply_markup"] = keyboard
    requests.post(url, json=payload)

# Функция для отправки инвойса для пополнения баланса
def send_invoice(chat_id):
    url = f"{BASE_URL}/sendInvoice"
    payload = {
        "chat_id": chat_id,
        "title": "Покупка звёзд",
        "description": "Купи звёзды для игры в RandomGift Casino!",
        "payload": "stars_payment",
        "provider_token": os.environ.get("PAYMENT_PROVIDER_TOKEN"),  # Токен от платежного провайдера
        "currency": "USD",
        "prices": [{"label": "100 звёзд", "amount": 500}],  # Пример: $5.00 за 100 звёзд (указываются в копейках)
        "start_parameter": "buy_stars",
        "photo_url": "https://example.com/star_image.png"  # URL изображения (замени на реальное)
    }
    requests.post(url, json=payload)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip()
        user = get_user(chat_id)
        if not user:
            create_user(chat_id)
            user = get_user(chat_id)

        if text == "/start":
            keyboard = {
                "keyboard": [
                    [{"text": "🎰 Крутить"}],
                    [{"text": "💰 Пополнить звёзды"}, {"text": "📊 Баланс"}]
                ],
                "resize_keyboard": True
            }
            welcome = (
                "🎲 Добро пожаловать в <b>RandomGift Casino</b>!\n\n"
                "У тебя есть возможность выиграть оригинальные коллекционные подарки Telegram.\n"
                "Для начала нажми <b>🎰 Крутить</b> (ставка 100 звёзд) или пополни баланс, нажав <b>💰 Пополнить звёзды</b>."
            )
            send_message(chat_id, welcome, keyboard)

        elif text == "🎰 Крутить":
            if user["stars"] >= 100:
                prize = get_random_prize()
                update_user_stars(chat_id, -100)  # Списываем ставку
                update_user_stars(chat_id, prize["value"])  # Начисляем выигрыш (может быть как в плюс, так и в минус)
                response = (
                    f"🎁 Твой спин завершился!\n"
                    f"Ты выиграл: <b>{prize['name']}</b>\n\n"
                    f"Ты получаешь: {prize['value']} звёзд."
                )
                send_message(chat_id, response)
            else:
                send_message(chat_id, "🚫 Недостаточно звёзд. Пополни баланс через кнопку <b>💰 Пополнить звёзды</b>.")

        elif text == "💰 Пополнить звёзды":
            send_invoice(chat_id)

        elif text == "📊 Баланс":
            send_message(chat_id, f"💰 Твой баланс: {user['stars']} звёзд.")

        else:
            send_message(chat_id, "Неизвестная команда. Используй /start, 🎰 Крутить, 💰 Пополнить звёзды или 📊 Баланс.")
    return {"ok": True}

if __name__ == "__main__":
    app.run()
