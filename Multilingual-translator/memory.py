import sqlite3

DB_NAME = "translator_memory.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input TEXT,
            output TEXT,
            target_lang TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_translation(user_input, translated_text, target_lang):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO translations (input, output, target_lang)
        VALUES (?, ?, ?)
    ''', (user_input, translated_text, target_lang))
    conn.commit()
    conn.close()

def get_all_translations():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM translations')
    data = c.fetchall()
    conn.close()
    return data

def clear_translations():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM translations')
    conn.commit()
    conn.close()
