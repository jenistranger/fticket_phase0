import sqlite3

DATABASE = 'bot_database.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        coins INTEGER DEFAULT 0,
                        tasks_completed INTEGER DEFAULT 0,
                        is_premium BOOLEAN DEFAULT 0,
                        has_received_initial_coins BOOLEAN DEFAULT 0
                      )''')
    conn.commit()
    conn.close()

def add_or_update_user(user_id: int, is_premium: bool):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''INSERT OR REPLACE INTO users (user_id, coins, tasks_completed, is_premium, has_received_initial_coins)
                      VALUES (?, 
                              COALESCE((SELECT coins FROM users WHERE user_id = ?), 0), 
                              COALESCE((SELECT tasks_completed FROM users WHERE user_id = ?), 0), 
                              ?, 
                              COALESCE((SELECT has_received_initial_coins FROM users WHERE user_id = ?), 0))''', 
                   (user_id, user_id, user_id, is_premium, user_id))
    conn.commit()
    conn.close()

def get_user_balance(user_id: int) -> int:
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT coins FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def update_user_tasks_and_coins(user_id: int, tasks_increment: int, coins_increment: int):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''UPDATE users
                      SET tasks_completed = tasks_completed + ?,
                          coins = coins + ?
                      WHERE user_id = ?''',
                   (tasks_increment, coins_increment, user_id))
    conn.commit()
    conn.close()

def set_initial_coins_received(user_id: int):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''UPDATE users
                      SET has_received_initial_coins = 1
                      WHERE user_id = ?''',
                   (user_id,))
    conn.commit()
    conn.close()

def has_user_received_initial_coins(user_id: int) -> bool:
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT has_received_initial_coins FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else False
