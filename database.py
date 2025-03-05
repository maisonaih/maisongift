import sqlite3

DB_NAME = "casino.db"

def connect_db():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_table():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            stars INTEGER DEFAULT 0
        )
    """)
    db.commit()
    db.close()

def get_user(chat_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE chat_id = ?", (chat_id,))
    row = cursor.fetchone()
    db.close()
    if row:
        return {"chat_id": row[0], "stars": row[1]}
    return None

def create_user(chat_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (chat_id, stars) VALUES (?, ?)", (chat_id, 0))
    db.commit()
    db.close()

def update_user_stars(chat_id, amount):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("UPDATE users SET stars = stars + ? WHERE chat_id = ?", (amount, chat_id))
    db.commit()
    db.close()

create_table()
