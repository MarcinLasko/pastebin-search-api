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

def save_paste(url, content):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    now = datetime.utcnow().isoformat()
    try:
        c.execute("INSERT INTO pastes (url, content, timestamp) VALUES (?, ?, ?)", (url, content, now))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Ignore duplicates
    conn.close()

def search_pastes(query):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT url, content, timestamp FROM pastes WHERE content LIKE ? ORDER BY timestamp DESC", (f"%{query}%",))
    results = [
        {"link": row[0], "snippet": get_snippet(row[1], query), "timestamp": row[2]}
        for row in c.fetchall()
    ]
    conn.close()
    return results

def get_snippet(text, query):
    idx = text.lower().find(query.lower())
    if idx == -1:
        return ""
    start = max(0, idx - 30)
    end = min(len(text), idx + 30)
    return text[start:end].replace('\n', ' ')
