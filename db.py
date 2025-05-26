import sqlite3
from datetime import datetime

DB_NAME = 'pastes.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pastes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            content TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()
