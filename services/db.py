import sqlite3
from datetime import datetime
from typing import Optional

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

    def search_messages(
            self,
            keyword: Optional[str] = None,
            date_from: Optional[str] = None,
            date_to: Optional[str] = None,
            limit: int = 100,
    ) -> list[dict]:
        """
        Search messages by keyword and/or date range.

        Dates must be YYYY-MM-DD.
        """

        query = """
               SELECT
                   id,
                   session_id,
                   role,
                   content,
                   created_at
               FROM messages
               WHERE 1 = 1
           """

        params = []

        # Search by text
        if keyword and keyword.strip():
            query += """
                   AND LOWER(content) LIKE LOWER(?)
               """
            params.append(f"%{keyword.strip()}%")

        # From date
        if date_from:
            datetime.strptime(date_from, "%Y-%m-%d")

            query += """
                   AND created_at >= ?
               """
            params.append(f"{date_from}T00:00:00")

        # To date
        if date_to:
            datetime.strptime(date_to, "%Y-%m-%d")

            query += """
                   AND created_at <= ?
               """
            params.append(f"{date_to}T23:59:59")

        query += """
               ORDER BY created_at ASC
               LIMIT ?
           """

        params.append(limit)

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            rows = conn.execute(query, params).fetchall()

        return [
            {
                "id": row["id"],
                "session_id": row["session_id"],
                "role": row["role"],
                "content": row["content"],
                "created_at": row["created_at"],
            }
            for row in rows
        ]

    def save_message(self, session_id: str, role: str, content: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO messages (session_id, role, content, created_at) VALUES (?, ?, ?, ?)',
                (session_id, role, content, datetime.now().isoformat())
            )
            conn.commit()
