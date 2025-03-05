import random

# Список подарков с разными значениями (плюс или минус звёзды)
PRIZES = [
    {"name": "Оригинальный стикер Telegram", "value": 15},
    {"name": "Редкий анимированный подарок", "value": 50},
    {"name": "Коллекционный подарок", "value": 300},
    {"name": "Сюрприз: подарок +200 звёзд", "value": 200},
    {"name": "Мега-приз: 1000 звёзд", "value": 1000},
    {"name": "Прокол: теряешь 50 звёзд", "value": -50}
]

def get_random_prize():
    return random.choice(PRIZES)
