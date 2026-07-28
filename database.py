import sqlite3

DB_NAME = "bot_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            username TEXT,
            plan TEXT DEFAULT 'Free',
            referred_by INTEGER,
            referral_count INTEGER DEFAULT 0,
            xp INTEGER DEFAULT 0,
            current_lang TEXT,
            current_level TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def add_user(user_id, first_name, username, referred_by=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (user_id, first_name, username, referred_by)
        VALUES (?, ?, ?, ?)
    ''', (user_id, first_name, username, referred_by))
    
    if referred_by and referred_by != user_id:
        cursor.execute("UPDATE users SET referral_count = referral_count + 1 WHERE user_id = ?", (referred_by,))
        
    conn.commit()
    conn.close()

def update_user_field(user_id, field, value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET {field} = ? WHERE user_id = ?", (value, user_id))
    conn.commit()
    conn.close()
