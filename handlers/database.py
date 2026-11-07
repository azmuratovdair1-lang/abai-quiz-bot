import sqlite3
import os

DB_PATH = "/data/quiz_bot.db" if os.path.exists("/data") else "quiz_bot.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            score INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def save_user_score(user_id: int, full_name: str, score: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT score FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()

    if row is None:
        cursor.execute("INSERT INTO users (user_id, full_name, score) VALUES (?, ?, ?)",
                       (user_id, full_name, score))
    else:
        cursor.execute("UPDATE users SET score = ?, full_name = ? WHERE user_id = ?",
                       (score, full_name, user_id))
    conn.commit()
    conn.close()

def get_top_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT full_name, score FROM users ORDER BY score DESC LIMIT 10")
    top_list = cursor.fetchall()
    conn.close()
    return top_list
