import sqlite3
from typing import List
from skills.communication.messages import Message
from .base_memory import BaseMemory

class LongTermMemory(BaseMemory):
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self._setup_db()

    def _setup_db(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT,
                importance INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def store(self, message: Message):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO memories (content, importance) VALUES (?, ?)",
                       (message.contenu, message.importance))
        self.conn.commit()

    def retrieve(self, query: str, max_results: int = 5) -> List[Message]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT content FROM memories
            WHERE content LIKE ?
            ORDER BY importance DESC, timestamp DESC LIMIT ?
        """, (f'%{query}%', max_results))
        rows = cursor.fetchall()
        return [Message(contenu=row[0]) for row in rows]

    def clear(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM memories")
        self.conn.commit()
