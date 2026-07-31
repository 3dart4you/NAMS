import sqlite3
from datetime import datetime

class ChatDatabase:
    def __init__(self, db_path: str = 'chat_history.db'):
        self.db_path = db_path

    def create_table(self):
       with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')
            conn.commit()

    def load_messages(self, session_id: str) -> list:
       with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT role, content, created_at FROM messages WHERE session_id = ? ORDER BY id', (session_id,))
            messages = [{"role": row[0], "content": row[1], "created_at": row[2]} for row in cursor.fetchall()]
            return messages

    def save_message(self, session_id: str, role: str, content: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO messages (session_id, role, content, created_at) VALUES (?, ?, ?, ?)',
                (session_id, role, content, datetime.now().isoformat())
            )
            conn.commit()
