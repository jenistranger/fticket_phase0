import sqlite3

DATABASE = 'bot_database.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        coins INTEGER DEFAULT 200,
                        tasks_completed INTEGER DEFAULT 0,
                        is_premium BOOLEAN DEFAULT 0
                      )''')
    conn.commit()
    conn.close()

def add_or_update_user(user_id: int, is_premium: bool):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''INSERT OR REPLACE INTO users (user_id, coins, tasks_completed, is_premium)
                      VALUES (?, 
                              COALESCE((SELECT coins FROM users WHERE user_id = ?), 200), 
                              COALESCE((SELECT tasks_completed FROM users WHERE user_id = ?), 0), 
                              ?)''', 
                   (user_id, user_id, user_id, is_premium))
    conn.commit()
    conn.close()

def get_user_balance(user_id: int) -> int:
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT coins FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0
